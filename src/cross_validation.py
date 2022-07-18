import glob
import os
import shutil
import json
import random
import warnings
import argparse
import numpy as np
from collections import defaultdict
from spacy.cli.convert import convert
from spacy.cli.train import train
from spacy.cli.evaluate import evaluate
from predict import Predict
from dataset import Dataset
from inter_dataset_agreement import measure_dataset, format_results
from json2SpacyJson import convertJsonToSpacyJsonl
from json2py import json_2_dict
from dataset2bratt import dataset_to_bratt
from validation_testing import execute

class CrossValidation:
    """
    A class to do k-fold cross validation for a Spacy model

    ...
    Attributes
    ----------
    self.k_folds : int
        number of folds
    self.tags : list[str]
        labels for ner entities

    Methods
    ----------
    create_config(self, name : str) -> str
        creates spacy model config file
    cross_validate(self, data : str, spacy_only : bool)
        preforms the k-fold cross validation
    predict(self, validation : list, fold : int, spacy_only : bool, model_dir : str, dataset_suffix : str)
        takes validation data and predicts
    medacy_eval(self)
        uses medacy to evaluate results
    print_metrics(self, metrics : dict, ents : dict)
        prints and formats metrics and entity counts
    count_entities()
        counts entities in gold standard data for each fold
    create_dirs(self, dirs : list)
        creates directories from a given list
    """
    def __init__(self, k_folds=5, tags=["ALAS", "CROP", "CVAR", "JRNL", "PATH", "PED", "PLAN", "PPTD", "TRAT"], sentence_level=False):
        self.k_folds = k_folds
        self.tags = tags
        warnings.filterwarnings('ignore')

    def create_config(self, name="senter_ner.cfg", gpu=False) -> str:
        """
        Creates spacy model config file

        Parameters
        ----------
        name : str
            path for config file
        gpu : bool
            flag to use GPU
        returns path to config file
        """
        if gpu:
            execute("python3 -m spacy init config --lang en --pipeline transformer,senter,ner  --optimize accuracy --force " + name +" -G")
        else:
            execute("python3 -m spacy init config --lang en --pipeline tok2vec,senter,ner  --optimize accuracy --force " + name)
        return name

    def cross_validate(self, data : str, config : str, model_dir_prefix="cv_model", sentence_level=False):
        """
        Preforms cross validation on spacy model.

        Parameters
        ----------
        data : str
            directory name where data is found
        config : str
            path to the model config file
        model_dir_prefix : str
            start of output path for the model, each fold creates a model with
            that prefix and the suffix of _XFold where X is the fold number
        sentence_level : bool
            if bratt conversion should take place on the sentence level
        """
        # shuffles and divides data into k folds and a dev set
        print("\nShuffling and splitting data...")
        splits = self.k_folds + 1
        files = glob.glob(data+"/**/*.json", recursive=True)
        random.shuffle(files)
        files_per_divison = (len(files) // splits)
        folds = []
        start,end = 0,1
        for i in range(0, splits):
            if i != splits-1:
                folds.append(files[files_per_divison*start:files_per_divison*end])
                start += 1
                end += 1
            else:
                folds.append(files[files_per_divison*start:len(files)])

        # makes spacy binary output dir
        self.create_dirs(["ner_2021_08"])

        # create and convert the dev set
        # this is used for every fold's spacy training & doesn't change
        print("\nCreating and converting dev data...")
        print("____________________________")
        dev = folds[len(folds)-1]
        convertJsonToSpacyJsonl(outputFileName="ner_2021_08_dev_data.jsonl", filePaths=dev)
        convert(input_path="ner_2021_08_dev_data.jsonl", output_dir="ner_2021_08", converter="json", file_type="spacy")

        # k-fold cross validation
        for f in range(1, self.k_folds+1):
            print("\n\nFOLD %s:" %f)

            # train - validate split
            training = []
            for i in range(0, self.k_folds):
                if i != f:
                    training += folds[i]
            validation = folds[f]

            # convert training data into spacy json and then into spacy binary
            print("\nConverting training data...")
            print("____________________________")
            convertJsonToSpacyJsonl(outputFileName="ner_2021_08_training_data.jsonl", filePaths=training)
            convert(input_path="ner_2021_08_training_data.jsonl", output_dir="ner_2021_08", converter="json", file_type="spacy")

            # evaulate model on validation data
            # model_name = model_dir_prefix
            model_name = "senter_ner_model/senter_ner_2021_08_model"
            fold_dir, gold_bratt_dir = self.create_gold_dataset(validation, f, sentence_level)

            # train model
            # train(config_path=config, output_path=model_name, overrides={"paths.train": "ner_2021_08/ner_2021_08_training_data.spacy", "paths.dev": "ner_2021_08/ner_2021_08_dev_data.spacy"})

            # spacy only
            print("\nEvaluating with spacy only...")
            print("____________________________")
            self.predict(fold_dir, "spacy", gold_bratt_dir, model_name+"/model-best", sentence_level)
            spacy_results = measure_dataset(Dataset("fold_"+str(f)+"_results/gold_bratt"), Dataset("fold_"+str(f)+"_results/spacy/pred_bratt"), 'strict')
            print("\nFold %s results with spacy only: " %f)
            print("____________________________")
            print(format_results(spacy_results))

            # spacy + pos tagging
            print("\nEvaluating with spacy & pos...")
            print("____________________________")
            self.predict(fold_dir, "pos", gold_bratt_dir, model_name+"/model-best", sentence_level)
            pos_results = measure_dataset(Dataset("fold_"+str(f)+"_results/gold_bratt"), Dataset("fold_"+str(f)+"_results/pos/pred_bratt"), 'strict')
            print("\nFold %s results with POS tagging: " %f)
            print("____________________________")
            print(format_results(pos_results))

        # average metrics and print
        spacy_avg_metrics, spacy_ents_found, spacy_ent_counts = self.medacy_eval("spacy")
        print("Spacy only results")
        print("____________________________")
        self.print_metrics(spacy_avg_metrics, spacy_ents_found, spacy_ent_counts)
        print()

        print("Spacy & POS tagging entity expansion results")
        print("____________________________")
        pos_avg_metrics, pos_ents_found, pos_ent_counts = self.medacy_eval("pos")
        self.print_metrics(pos_avg_metrics, pos_ents_found, pos_ent_counts)

    def create_gold_dataset(self, validation : list, fold : int, sentence_level : bool):
        """
        validation : list
            list of file names to use for validation
        fold : int
            current fold, used for directory naming
        """
        fold_dir = "fold_" + str(fold) + "_results"
        gold_json_name = fold_dir + "/gold_json"
        gold_bratt_name = fold_dir + "/gold_bratt"
        self.create_dirs([fold_dir, gold_json_name, gold_bratt_name])
        # create and convert to bratt gold standard dataset
        print("\nCreating gold standard validation dataset...")
        for file in validation:
            json_file = open(file)
            contents = json.load(json_file)
            name_split = file.split("/")
            file_name = name_split[len(name_split)-1]
            with open(gold_json_name+"/"+file_name, 'w') as f:
                json.dump(contents, f)
        print("\nConverting gold standard to bratt...")
        print("____________________________")
        dataset_to_bratt(input_dir=gold_json_name, output_dir=gold_bratt_name, sentence_level=sentence_level)
        return fold_dir, gold_bratt_name

    def predict(self, fold_dir, sub_dir, gold_dir, model_dir, sentence_level):
        """
        For a given fold, predicts on the validation data and saves to json.
        Also moves the gold standard validation data in json format to a new
        directory. Then converts both of these datasets to bratt format.

        Parameters
        ----------
        fold_dir : str
            path to output predictions for this fold to
        sub_dir : str
            path to subdirectory for output, either "pos" or "spacy"
        gold_dir : str
            path to gold standard dataset
        model_dir : str
            path to model to do predictions with
        """
        # create output directories
        print("\nCreating output directories...")
        json_name = fold_dir + "/" + sub_dir + "/pred_json"
        bratt_name = fold_dir + "/" + sub_dir + "/pred_bratt"
        self.create_dirs([json_name, bratt_name])

        if sub_dir == "spacy":
            flag = True
        else:
            flag = False

        # do pos tagging  entity expansion
        print("Predicting on validation data ...")
        print("____________________________")
        predict = Predict(model_dir=model_dir, dataset_dir=gold_dir, output_dir=json_name, spacy_only=flag)
        predict.process_files()

        # convert predictions to bratt format
        print("\nConverting predictions to bratt...")
        print("____________________________")
        dataset_to_bratt(input_dir=json_name, output_dir=bratt_name, sentence_level=sentence_level)


    def medacy_eval(self, sub_dir):
        """
        Finds average metrics and entity counts across all folds.
        Uses medacy's inter_dataset_agreement calculator to get
        precesion, recall, and f-score for each label and overall for each fold.
        Then finds averages of those metrics across every folds. Also keeps
        track of found entity counts and entitiy counts from gold standard.

        Returns dictonary of average metrics, found entity counts, and
        count of entities found in gold standard data.
        """
        avg_metrics, ents_found = defaultdict(), defaultdict()
        ent_counts = self.count_entities()
        p_all, r_all, f_all = [], [], []
        p_weights, r_weights, f_weights = [], [], []

        # inter_dataset_agreement for each fold
        ents_found["ALL"] = 0
        for f in range(1, self.k_folds+1):
            result = measure_dataset(Dataset("fold_"+str(f)+"_results/gold_bratt"), Dataset("fold_"+str(f)+"_results/"+sub_dir+"/pred_bratt"), 'strict')
            for k,v in result.items():
                p_all.append(v.precision())
                p_weights.append(ent_counts[f][k])

                r_all.append(v.recall())
                r_weights.append(ent_counts[f][k])

                f_all.append(v.f_score())
                f_weights.append(ent_counts[f][k])

                avg_metrics[k] = [[v.precision()], [v.recall()], [v.f_score()]]
                if k not in ents_found.keys():
                    ents_found[k] = v.tp + v.fp
                else:
                    ents_found[k] += v.tp + v.fp
                ents_found["ALL"] += v.tp + v.fp

        # averaging
        avg_metrics["ALL"] = {}
        avg_metrics["ALL"][0] = np.average(a=p_all, weights=p_weights)
        avg_metrics["ALL"][1] = np.average(a=r_all, weights=r_weights)
        avg_metrics["ALL"][2] = np.average(a=r_all, weights=r_weights)
        ents_found["ALL AVG"] = ents_found["ALL"] / self.k_folds
        ent_counts["ALL AVG"] = ent_counts["ALL"] / self.k_folds

        for k,v in avg_metrics.items():
            if k != "ALL":
                avg_metrics[k][0] = sum(avg_metrics[k][0]) / len(avg_metrics[k][0])
                avg_metrics[k][1] = sum(avg_metrics[k][1]) / len(avg_metrics[k][1])
                avg_metrics[k][2] = sum(avg_metrics[k][2]) / len(avg_metrics[k][2])
                ents_found[k+" AVG"] = ents_found[k] / self.k_folds
                ent_counts[k + " AVG"] = ent_counts[k+" SUM"] / self.k_folds

        return avg_metrics, ents_found, ent_counts

    def print_metrics(self, metrics : dict, ents_found : dict, counts : dict):
        """
        Takes a dictonary of averages & entity counts created by medacy_eval()
        and formats & prints the averages and counts.

        Parameters
        ----------
        metrics : dict
            dictonary of the averaged metrics from medacy_eval()
        ents : dict
            dictonary of found entity counts from medacy_eval()
        counts : dict
            dictonary of toatl entity counts in gold standard from count_entities()
        """
        print("ALL:")
        print("\t precision: " + str(metrics["ALL"][0]))
        print("\t recall: " +  str(metrics["ALL"][1]))
        print("\t F1: " +  str(metrics["ALL"][2]))
        print("\t found across all folds: " + str(ents_found["ALL"]))
        print("\t entities found per fold: " + str(ents_found["ALL AVG"]))
        print()
        print("\t entities across all folds: " + str(counts["ALL"]))
        print("\t average entities per fold: " + str(counts["ALL AVG"]))
        print("\n")
        for k,v in sorted(metrics.items()):
            if k != "ALL":
                print(k+":")
                print("\t precision: " + str(metrics[k][0]))
                print("\t recall: " + str(metrics[k][1]))
                print("\t F1: " + str(metrics[k][2]))
                print("\t found across all folds: " + str(ents_found[k]))
                print("\t average found per fold: " + str(ents_found[k+ " AVG"]))
                print()
                print("\t entities across all folds: " + str(counts[k+" SUM"]))
                print("\t average entities per fold: " + str(counts[k+ " AVG"]))
                print("\n")

    def count_entities(self):
        """
        Counts number of entities in gold standard data for each fold.

        Returns dictonary of entity counts.
        """
        counts = defaultdict()
        counts["ALL"] = 0
        for f in range(1, self.k_folds+1):
            current_dir = "fold_" + str(f) + "_results/gold_json"
            files = glob.glob(current_dir+"/*.json", recursive=True)
            counts[f] = defaultdict()
            for file in files:
                with open(file) as j:
                    data = json.load(j)
                key = list(data["sentences"].keys())[0]
                for ent in data["sentences"][key]:
                    lab = data["sentences"][key][ent]["label"]
                    if lab in self.tags:
                        if lab not in counts[f].keys():
                            counts[f][lab] = 1
                        else:
                            counts[f][lab] += 1

                        if lab+" SUM" not in counts.keys():
                            counts[lab+" SUM"] = 1
                        else:
                            counts[lab+" SUM"] += 1
                        counts["ALL"] += 1
        return counts

    def create_dirs(self, dirs : list):
        """
        Takes a list of directories, and for if it
        doesn't exist, creates a new directory and if it does exist, deletes the
        current one and creates a new empty one. Unless specified in the
        directory's name, creates the new directory in the current directory.

        Parameters
        ----------
        dirs : list[str]
            list of directories to create, can be a list of just one directory,
            if only one needs to be created.
        """
        for dir in dirs:
            if not os.path.exists(dir):
                os.makedirs(dir)
            else:
                shutil.rmtree(dir)
                os.makedirs(dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Spacy cross validation",
        epilog='python crossvalidation.py Data/dataset_dir --folds 5 --spacy_only'
    )
    parser.add_argument(
        'dataset_dir', help='path to dataset'
    )
    parser.add_argument(
        '--folds',
        action='store', default=5,
        help='number of folds'
    )
    parser.add_argument(
        '--GPU',
        action='store_true', default=False,
        help='wether or not to use GPU'
    )
    parser.add_argument(
        '--sentence_level',
        action='store_true', default=False,
        help='flag for sentence level annotations'
    )

    args = parser.parse_args()

    val = CrossValidation(k_folds=int(args.folds))
    config_name = val.create_config(gpu=args.GPU)
    val.cross_validate(data=args.dataset_dir, config=config_name, sentence_level=args.sentence_level)
