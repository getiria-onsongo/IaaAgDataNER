# must pip install tabulate!
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
from crf_component import create_crf_component
from json2SpacyJson import convertJsonToSpacyJsonl
from json2py import json_2_dict

from dataset2bratt import dataset_to_bratt
from add_ents_to_spans_dict import convert_to_span
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
    self.pos : bool
        flag to do POS-tagging based entity expansion
    self.spancat : bool
        flag to use spancat SpaCy component instead of the normal ner component,
        not done implementing yet

    Methods
    ----------
    create_config(self, name : str, model_name : str, gpu : bool, word_embed : bool, vectors : str) -> str
        creates spacy config file
    cross_validate(self, data : str, config : str, model_name : str)
        preforms k-fold cross validation
    predict(self, fold_dir : str, sub_dir : str, gold_dir : str, model_dir : str)
        predicts with trained model on validation data
    medacy_eval(self, sub_dir)
        evaluate results
    print_metrics(self, metrics : dict, ents : dict)
        prints metrics & entity counts
    create_gold_dataset(self, validation : list, fold : int)
        creates gold standard dataset
    count_entities(self)
        counts entities in gold standard data
    create_dirs(self, dirs : list)
        creates directories
    """
    def __init__(self, k_folds=5, pos=False, spancat=False, tags=["ALAS", "CROP", "CVAR", "JRNL", "PATH", "PED", "PLAN", "PPTD", "TRAT"]):
        self.k_folds = k_folds
        self.tags = tags
        self.pos = pos
        self.spancat = spancat
        warnings.filterwarnings('ignore') # ignore SpaCy warnings for cleaner terminal output

    def create_config(self, name="senter_ner.cfg", model_name="cv_model", gpu=False, word_embed=False, vectors=
    "glove.6B.zip") -> str:
        """
        Creates spacy model config file to use to train the model

        Parameters
        ----------
        name : str
            path to config file
        model_name : str
            path to model directory
        gpu : bool
            flag to use GPU
        word_embed : bool
            flag to use word embeddings
        vectors : str
            path to word embeddings

        Returns path to config file
        """
        if gpu:
            execute("python3 -m spacy init config --lang en --pipeline transformer,senter,ner  --optimize accuracy --force " + name + " -G")
        elif word_embed:
            execute("python3 -m spacy init config --lang en --pipeline tok2vec,senter,ner  --optimize accuracy --force " + name)
            execute("python3 -m spacy init vectors en " + vectors + " " + model_name)
        elif self.spancat:
            execute("python3 -m spacy init config --lang en --pipeline tok2vec,senter,spancat  --optimize accuracy --force " + name)
        else:
            execute("python3 -m spacy init config --lang en --pipeline tok2vec,senter,ner  --optimize accuracy --force " + name)

        return name

    def cross_validate(self, data : str, config : str, crf=False, model_name="cv_model"):
        """
        Preforms k-fold cross validation on spacy model since SpaCy does not support
        it out of the box

        Parameters
        ----------
        data : str
            path to data directory
        config : str
            path to model config file
        model_name : str
            path to save model, overwritten during the subsequent fold
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
        if self.spancat:
            convert_to_span("ner_2021_08/ner_2021_08_dev_data.spacy", "en", "sc")

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
            if self.spancat:
                convert_to_span("ner_2021_08/ner_2021_08_training_data.spacy", "en", "sc")

            # model_name = "cv_model" # for testing only
            # create gold standard data directory and bratt files
            fold_dir, gold_bratt_dir = self.create_gold_dataset(validation, f)

            # train model
            train(config_path=config, output_path=model_name, overrides={"paths.train": "ner_2021_08/ner_2021_08_training_data.spacy", "paths.dev": "ner_2021_08/ner_2021_08_dev_data.spacy"})

            if crf:
                nlp = create_crf_component(spacy.load(model_name), training)
                nlp.to_disk(model_name)

            # spacy only predictions on validation data
            print("\nEvaluating with spacy only...")
            print("____________________________")
            self.predict(crf, fold_dir, "spacy", gold_bratt_dir, model_name+"/model-best")
            spacy_results = measure_dataset(Dataset("fold_"+str(f)+"_results/gold_bratt"), Dataset("fold_"+str(f)+"_results/spacy/pred_bratt"), 'strict')
            print("\nFold %s results with spacy only: " %f)
            print("____________________________")
            print(format_results(spacy_results))

            if self.pos:
                # spacy + pos tagging predictions on validation data
                print("\nEvaluating with spacy & pos...")
                print("____________________________")
                self.predict(crf, fold_dir, "pos", gold_bratt_dir, model_name+"/model-best")
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

        if self.pos:
            print("Spacy & POS tagging entity expansion results")
            print("____________________________")
            pos_avg_metrics, pos_ents_found, pos_ent_counts = self.medacy_eval("pos")
            self.print_metrics(pos_avg_metrics, pos_ents_found, pos_ent_counts)

    def predict(self, crf : bool, fold_dir : str, sub_dir : str, gold_dir : str, model_dir : str):
        """
        For a given fold, uses trained model to predict on the validation data
        Then saves to json before converting bratt

        Parameters
        ----------
        fold_dir : str
            path to save currenft fold's predictions to
        sub_dir : str
            path to subdirectory of fold_dir for output, either "pos" or "spacy"
        gold_dir : str
            path to gold standard dataset for the current fold
        model_dir : str
            path to model
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

        # predict using trained model
        print("Predicting on validation data ...")
        print("____________________________")
        predict = Predict(model_dir=model_dir, dataset_dir=gold_dir, crf=crf, spancat=self.spancat, output_dir=json_name, spacy_only=flag)
        predict.process_files()

        # convert predictions to bratt format
        print("\nConverting predictions to bratt...")
        print("____________________________")
        dataset_to_bratt(input_dir=json_name, output_dir=bratt_name)

    def medacy_eval(self, sub_dir):
        """
        Finds average metrics and entity counts across all folds using extracted
        methods from medacy

        Parameters
        ----------
        sub_dir : str
            current sub directory for predictions evaluating with, either pos
            or spacy

        Returns dictonary of average metrics, found entity counts, and
        count of entities found in gold standard data.
        """
        avg_metrics, ents_found = defaultdict(), defaultdict()
        ent_counts = self.count_entities()
        p_all, r_all, f_all = [], [], []
        p_weights, r_weights, f_weights = [], [], []

        # inter_dataset_agreement and entity counting for each fold
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

        # get averages
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
        to format & print the averages and counts

        Parameters
        ----------
        metrics : dict
            dictonary of the averaged metrics from medacy_eval()
        ents : dict
            dictonary of found entity counts from medacy_eval()
        counts : dict
            dictonary of total entity counts in gold standard from count_entities()
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

    def create_gold_dataset(self, validation : list, fold : int):
        """
        Creates gold standard dataset for current fold and converts to bratt

        Parameters
        ----------
        validation : list
            list of file names to use for validation
        fold : int
            current fold, used for directory naming

        Returns name of directory for current fold and name of directory for
        bratt format gold standard data for this fold.
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
        dataset_to_bratt(input_dir=gold_json_name, output_dir=gold_bratt_name)

        return fold_dir, gold_bratt_name

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
            if only one needs to be created
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
        '--pos',
        action='store_true', default=False,
        help='pos based entity expansion flag'
    )
    parser.add_argument(
        '--spancat',
        action='store_true', default=False,
        help='flag to use spancat instead of ner component in spacy'
    )
    parser.add_argument(
        '--GPU',
        action='store_true', default=False,
        help='flag to use GPU'
    )
    parser.add_argument(
        '--word_embed',
        action='store_true', default=False,
        help='flag to use word emeddings'
    )
    parser.add_argument(
        '--vectors',
        action='store', default=None,
        help='path to vectors'
    )
    parser.add_argument(
        '--crf',
        action='store_true', default=False,
        help='flag for crf layers'
    )
    args = parser.parse_args()
    val = CrossValidation(k_folds=int(args.folds), pos=args.pos, spancat=args.spancat)
    config_name = val.create_config(gpu=args.GPU, word_embed=args.word_embed, vectors=args.vectors)
    val.cross_validate( data=args.dataset_dir, config=config_name, crf=args.crf)
