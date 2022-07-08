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
    cross_validate(self, data : str, pos_split : bool)
        preforms the k-fold cross validation
    extract_metrics(self, prefix="metrics_fold", suffix=".json") -> dict
        for json files created from spacy evaluation, extracts into dictionary
    average_metrics(self, metrics : dict) -> dict
        averages values across folds for dictonary created in extract_metrics
    format_metrics(self, metrics : dict)
        prints formated contents of dictonary created in average_metrics
    create_dirs(self, dirs : list)
        creates directories from a given list
    """
    def __init__(self, k_folds=5, tags=["ALAS", "CROP", "CVAR", "JRNL", "PATH", "PED", "PLAN", "PPTD", "TRAT"]):
        self.k_folds = k_folds
        self.tags = tags
        warnings.filterwarnings('ignore')

    def cross_validate(self, data : str, spacy_only : bool):
        """
        Preforms cross validation on spacy model.

        Parameters
        ----------
        data : str
            directory name where data is found
        pos_split : bool
            flag to do pos tagging and entity expansion
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
        for v in range(0, self.k_folds):
            print("\nOn fold %s:" %fold_counter)
            fold_counter += 1
            # train - validate split
            training = []
            for t in range(0, self.k_folds):
                if t != v:
                    training += folds[t]
            validation = folds[v]

            # convert training data into spacy json and then into spacy binary
            print("\nConverting training data...")
            print("____________________________")
            convertJsonToSpacyJsonl(outputFileName="ner_2021_08_training_data.jsonl", filePaths=training)
            convert(input_path="ner_2021_08_training_data.jsonl", output_dir="ner_2021_08", converter="json", file_type="spacy")

            # train model
            train(config_path="senter_ner.cfg", output_path="senter_ner_model", overrides={"paths.train": "ner_2021_08/ner_2021_08_training_data.spacy", "paths.dev": "ner_2021_08/ner_2021_08_dev_data.spacy"})

            # evaulate model
            self.predict(validation, v, spacy_only)
        # average metrics and print
        avgs, ents = self.medacy_eval()
        self.format_metrics(avgs, ents)

    def predict(self, validation : list, v : int, spacy_only : bool):
        print("\nCreating output directories...")
        # create output directories
        fold_dir = "fold_" + str(v) + "_results"
        json_name = fold_dir + "/pred_json"
        bratt_name = fold_dir + "/pred_bratt"
        gold_json_name = fold_dir + "/gold_json"
        gold_bratt_name = fold_dir + "/gold_bratt"
        self.create_dirs([fold_dir, json_name, bratt_name, gold_json_name, gold_bratt_name])

        # do pos tagging & entity expansion
        print("Predicting on validation data...")
        predict = Predict(model_dir="senter_ner_model/model-best", output_dir=json_name, dataset_suffix="_td.json", spacy_only=spacy_only)
        predict.process_files(validation, json=True)

        # create gold standard dataset and convert both to bratt
        # can now be run through medacy's inter_dataset_agreement tool for evaulation
        print("Creating gold standard validation dataset...")
        for file in validation:
            json_file = open(file)
            contents = json.load(json_file)
            ls = file.split("/")
            file_name = ls[len(ls)-1]
            with open(gold_json_name+"/"+file_name, 'w') as f:
                json.dump(contents, f)

        print("Converting to bratt...")
        dataset_to_bratt(gold_json_name, gold_bratt_name)
        dataset_to_bratt(json_name, bratt_name)

    def medacy_eval(self):
        avg_metrics = defaultdict()
        ents = defaultdict()
        ents["ALL"] = []
        p_all = []
        r_all = []
        f_all = []

        ent_counter = 0
        result0 = measure_dataset(Dataset("fold_0_results/gold_bratt"), Dataset("fold_0_results/pred_bratt"), 'strict')
        for k,v in result0.items():
            p_all.append(v.precision())
            r_all.append(v.recall())
            f_all.append(v.f_score())
            avg_metrics[k] = [[v.precision()], [v.recall()], [v.f_score()]]
            ent_counter += v.tp + v.tn + v.fp + v.fn
            ents[k] = [v.tp + v.tn + v.fp + v.fn]
        ents["ALL"].append(ent_counter)
        ent_counter = 0

        result1 = measure_dataset(Dataset("fold_1_results/gold_bratt"), Dataset("fold_1_results/pred_bratt"), 'strict')
        for k,v in result1.items():
            p_all.append(v.precision())
            r_all.append(v.recall())
            f_all.append(v.f_score())
            avg_metrics[k][0].append(v.precision())
            avg_metrics[k][1].append(v.recall())
            avg_metrics[k][2].append(v.f_score())
            ent_counter += v.tp + v.tn + v.fp + v.fn
            ents[k].append(v.tp + v.tn + v.fp + v.fn)
        ents["ALL"].append(ent_counter)
        ent_counter = 0

        result2 = measure_dataset(Dataset("fold_2_results/gold_bratt"), Dataset("fold_2_results/pred_bratt"), 'strict')
        for k,v in result2.items():
            p_all.append(v.precision())
            r_all.append(v.recall())
            f_all.append(v.f_score())
            avg_metrics[k][0].append(v.precision())
            avg_metrics[k][1].append(v.recall())
            avg_metrics[k][2].append(v.f_score())
            ent_counter += v.tp + v.tn + v.fp + v.fn
            ents[k].append(v.tp + v.tn + v.fp + v.fn)
        ents["ALL"].append(ent_counter)
        ent_counter = 0

        result3 = measure_dataset(Dataset("fold_3_results/gold_bratt"), Dataset("fold_3_results/pred_bratt"), 'strict')
        for k,v in result3.items():
            p_all.append(v.precision())
            r_all.append(v.recall())
            f_all.append(v.f_score())
            avg_metrics[k][0].append(v.precision())
            avg_metrics[k][1].append(v.recall())
            avg_metrics[k][2].append(v.f_score())
            ent_counter += v.tp + v.tn + v.fp + v.fn
            ents[k].append(v.tp + v.tn + v.fp + v.fn)
        ents["ALL"].append(ent_counter)
        ent_counter = 0

        result4 = measure_dataset(Dataset("fold_4_results/gold_bratt"), Dataset("fold_4_results/pred_bratt"), 'strict')
        for k,v in result4.items():
            p_all.append(v.precision())
            r_all.append(v.recall())
            f_all.append(v.f_score())
            avg_metrics[k][0].append(v.precision())
            avg_metrics[k][1].append(v.recall())
            avg_metrics[k][2].append(v.f_score())
            ent_counter += v.tp + v.tn + v.fp + v.fn
            ents[k].append(v.tp + v.tn + v.fp + v.fn)
        ents["ALL"].append(ent_counter)
        ent_counter = 0

        avg_metrics["ALL"] = [sum(p_all)/len(p_all), sum(r_all)/len(r_all), sum(f_all)/len(f_all)]
        ents["ALL AVG"] = sum(ents["ALL"]) / 5
        for k,v in avg_metrics.items():
            if k != "ALL":
                avg_metrics[k][0] = sum(avg_metrics[k][0]) / len(avg_metrics[k][0])
                avg_metrics[k][1] = sum(avg_metrics[k][1]) / len(avg_metrics[k][1])
                avg_metrics[k][2] = sum(avg_metrics[k][2]) / len(avg_metrics[k][2])
                ents[k+" AVG"] = sum(ents[k])/ 5
        return avg_metrics, ents

    def format_metrics(self, metrics : dict, ents : dict):
        """
        Takes a dictonary of metric averages, and formats & prints the metrics.

        Parameters
        ----------
        metrics : dict
            dictonary of the averaged metrics
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
        Takes a list of directories, and for each one checks if it exists, and
        if not creates the directory. Unless specified in the directory's name,
        creates the new directory in the current directory.

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
        epilog='python crossvalidation.py Data/dataset_dir --folds 5 --pos_tagging'
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
            action='store_true',
            default = False,
            help='only use spacy, no pos_tagging'
    )
    args = parser.parse_args()

    val = CrossValidation(k_folds=int(args.folds))
    val.cross_validate(args.dataset_dir, args.spacy_only)
