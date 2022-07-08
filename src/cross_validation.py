import glob
import os
import shutil
import json
import random
import warnings
import argparse
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
    create_dirs(self, dirs : list)
        creates directories from a given list
    """
    def __init__(self, k_folds=5, tags=["ALAS", "CROP", "CVAR", "JRNL", "PATH", "PED", "PLAN", "PPTD", "TRAT"]):
        self.k_folds = k_folds
        self.tags = tags
        warnings.filterwarnings('ignore')

    def create_config(self, name="senter_ner.cfg") -> str:
        """
        Creates spacy model config file

        Parameters
        ----------
        name : str
            path for config file
        returns path to config file
        """
        execute("python3 -m spacy init config --lang en --pipeline tok2vec,senter,ner  --optimize accuracy --force " + name)
        return name

    def cross_validate(self, data : str, spacy_only : bool, model_dir="senter_ner_model", config="senter_ner.cfg"):
        """
        Preforms cross validation on spacy model.

        Parameters
        ----------
        data : str
            directory name where data is found
        spacy_only : bool
            flag to only use spacy, not part of speech based entity expansion
        model_dir : str
            output path for the model, after each fold the model is just
            overwritten
        config : str
            path to the model config file
        """
        # shuffles and divides data into k folds and a dev set
        print("Shuffling and splitting data...")
        splits = self.k_folds + 1
        files = glob.glob(data+"/*.json") # add feature to search multiple dirs?
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

        # makes spacy binary output dir if it doesn't exist
        self.create_dirs(["ner_2021_08"])

        # create and convert the dev set
        # this is used for every fold's spacy training & doesn't change
        print("\nCreating and converting dev data...")
        print("____________________________")
        dev = folds[len(folds)-1]
        convertJsonToSpacyJsonl(outputFileName="ner_2021_08_dev_data.jsonl", filePaths=dev)
        convert(input_path="ner_2021_08_dev_data.jsonl", output_dir="ner_2021_08", converter="json", file_type="spacy")

        fold_counter = 1
        # k-fold cross validation
        for f in range(0, self.k_folds):
            print("\nOn fold %s:" %fold_counter)
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

            # train model
            train(config_path="senter_ner.cfg", output_path=model_dir, overrides={"paths.train": "ner_2021_08/ner_2021_08_training_data.spacy", "paths.dev": "ner_2021_08/ner_2021_08_dev_data.spacy"})

            # evaulate model
            self.predict(validation, f, spacy_only, model_dir+"/model-best")
            fold_results = measure_dataset(Dataset("fold_"+str(f)+"_results/gold_bratt"), Dataset("fold_"+str(f)+"_results/pred_bratt"), 'strict')
            print("Fold %s results: " %fold_counter)
            print(format_results(fold_results))
            fold_counter += 1

        # average metrics and print
        avgs, ents = self.medacy_eval()
        self.print_metrics(avgs, ents)

    def predict(self, validation : list, fold : int, spacy_only : bool, model_dir="senter_ner_model/model-best", dataset_suffix="_td.json"):
        """
        For a given fold, predicts on the validation data and saves to json.
        Also moves the gold standard validation data in json format to a new
        directory. Then converts both of these datasets to bratt format.

        Parameters
        ----------
        validation : list
            list of file names to use for validation
        fold : int
            current fold, used for directory naming
        spacy_only : bool
            if the model should only use spacy and not pos tagging & expansion
        model_dir : str
            path to spacy model to predict with
        dataset_suffix : str
            file ending of validation data
        """
        # create output directories
        print("\nCreating output directories...")
        fold_dir = "fold_" + str(fold) + "_results"
        json_name = fold_dir + "/pred_json"
        bratt_name = fold_dir + "/pred_bratt"
        gold_json_name = fold_dir + "/gold_json"
        gold_bratt_name = fold_dir + "/gold_bratt"
        self.create_dirs([fold_dir, json_name, bratt_name, gold_json_name, gold_bratt_name])

        # do pos tagging & entity expansion
        print("Predicting on validation data...")
        predict = Predict(model_dir=model_dir, output_dir=json_name, dataset_suffix=dataset_suffix, spacy_only=spacy_only)
        predict.process_files(validation, json=True)

        # create gold standard dataset
        print("Creating gold standard validation dataset...")
        for file in validation:
            json_file = open(file)
            contents = json.load(json_file)
            name_split = file.split("/")
            file_name = name_split[len(name_split)-1]
            with open(gold_json_name+"/"+file_name, 'w') as f:
                json.dump(contents, f)

        # convert gold standard & predictions to bratt format to use with medacy
        print("Converting to bratt...")
        dataset_to_bratt(gold_json_name, gold_bratt_name)
        dataset_to_bratt(json_name, bratt_name)

    def medacy_eval(self):
        """
        Finds average metrics and entity counts across all folds.
        Uses medacy's inter_dataset_agreement calculator to get
        precesion, recall, and f-score for each label and overall for each fold.
        Then finds averages of those metrics across every folds. Kkeeps track
        of entity counts (overall & for each label) for each fold and finds
        overall averages.

        Returns dictonary of average metrics and dictonary of entity counts.
        """
        avg_metrics = defaultdict()
        ents = defaultdict()
        ents["ALL"] = []
        p_all = []
        r_all = []
        f_all = []

        # inter_dataset_agreement for each fold
        for f in range(0, self.k_folds):
            ent_counter = 0
            result = measure_dataset(Dataset("fold_"+str(f)+"_results/gold_bratt"), Dataset("fold_"+str(f)+"_results/pred_bratt"), 'strict')
            for k,v in result.items():
                p_all.append(v.precision())
                r_all.append(v.recall())
                f_all.append(v.f_score())
                avg_metrics[k] = [[v.precision()], [v.recall()], [v.f_score()]]
                ent_counter += v.tp + v.tn + v.fp + v.fn
                ents[k] = [v.tp + v.tn + v.fp + v.fn]
            ents["ALL"].append(ent_counter)

        # averaging
        avg_metrics["ALL"] = [sum(p_all)/len(p_all), sum(r_all)/len(r_all), sum(f_all)/len(f_all)]
        ents["ALL AVG"] = sum(ents["ALL"]) / self.k_folds
        for k,v in avg_metrics.items():
            if k != "ALL":
                avg_metrics[k][0] = sum(avg_metrics[k][0]) / len(avg_metrics[k][0])
                avg_metrics[k][1] = sum(avg_metrics[k][1]) / len(avg_metrics[k][1])
                avg_metrics[k][2] = sum(avg_metrics[k][2]) / len(avg_metrics[k][2])
                ents[k+" AVG"] = sum(ents[k])/ self.k_folds

        return avg_metrics, ents

    def print_metrics(self, metrics : dict, ents : dict):
        """
        Takes a dictonary of averages & entity counts created by medacy_eval()
        and formats & prints the averages and counts.

        Parameters
        ----------
        metrics : dict
            dictonary of the averaged metrics from medacy_eval()
        ents : dict
            dictonary of entity counts from medacy_eval()
        """
        print("ALL:")
        print("\t precision: " + str(metrics["ALL"][0]))
        print("\t recall: " +  str(metrics["ALL"][1]))
        print("\t F1: " +  str(metrics["ALL"][2]))
        print("\t entities each fold: " + str(ents["ALL"]))
        print("\t average entities per fold: " + str(ents["ALL AVG"]))
        for k,v in metrics.items():
            if k != "ALL":
                print(k+":")
                print("\t precision: " + str(metrics[k][0]))
                print("\t recall: " + str(metrics[k][1]))
                print("\t F1: " + str(metrics[k][2]))
                print("\t entities each fold: " + str(ents[k]))
                print("\t average entities per fold: " + str(ents[k+ " AVG"]))

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
        '--spacy_only',
        action='store_true', default = False,
        help='only use spacy, no pos tagging & entity expansion'
    )
    args = parser.parse_args()

    val = CrossValidation(k_folds=int(args.folds))
    val.create_config()
    val.cross_validate(args.dataset_dir, args.spacy_only)
