import glob
import os
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

    def cross_validate(self, data : str, pos_tagging : bool):
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
            if pos_tagging:
                self.pos_tagging(validation, v)
            else:
                # convert validate data
                print("Converting validation data...")
                convertJsonToSpacyJsonl(outputFileName="ner_2021_08_validate_data.jsonl", filePaths=validation)
                convert(input_path="ner_2021_08_validate_data.jsonl", output_dir="ner_2021_08", converter="json", file_type="spacy")
                output_name = "metrics_fold" + str(v) + ".json"

                # evaluate
                print("Evaluating...")
                evaluate(model="ner_2021_08_model/model-best", data_path="ner_2021_08/ner_2021_08_validate_data.spacy", output=output_name)

        if pos_tagging:
            self.medacy_eval()


    def pos_tagging(self, validation : list, v : int):
        print("\nCreating output directories for POS entity expansion...")
        # create output directories
        fold_dir = "fold_" + str(v) + "_results"
        json_name = fold_dir + "/pred_json"
        bratt_name = fold_dir + "/pred_bratt"
        gold_json_name = fold_dir + "/gold_json"
        gold_bratt_name = fold_dir + "/gold_bratt"
        self.create_dirs([fold_dir, json_name, bratt_name, gold_json_name, gold_bratt_name])

        # do pos tagging & entity expansion
        print("Entity expansion post-processing...")
        predict = Predict(model_dir="senter_ner_model/model-best", output_dir=json_name, dataset_suffix="_td.json")
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
        print("Results from this fold are ready for Medacy!\n")

    def medacy_eval(self):
        print("Fold 0")
        print("____________________________")
        result = measure_dataset(Dataset("fold_0_results/gold_bratt"), Dataset("fold_0_results/pred_bratt"), 'strict')
        output = format_results(result)
        print(output)

        print("\nFold 1")
        print("____________________________")
        result = measure_dataset(Dataset("fold_1_results/gold_bratt"), Dataset("fold_1_results/pred_bratt"), 'strict')
        output = format_results(result)
        print(output)


        print("\nFold 2")
        print("____________________________")
        result = measure_dataset(Dataset("fold_2_results/gold_bratt"), Dataset("fold_2_results/pred_bratt"), 'strict')
        output = format_results(result)
        print(output)


        print("\nFold 3")
        print("____________________________")
        result = measure_dataset(Dataset("fold_3_results/gold_bratt"), Dataset("fold_3_results/pred_bratt"), 'strict')
        output = format_results(result)
        print(output)

        print("\nFold 4")
        print("____________________________")
        result = measure_dataset(Dataset("fold_4_results/gold_bratt"), Dataset("fold_4_results/pred_bratt"), 'strict')
        output = format_results(result)
        print(output)

    def extract_metrics(self, prefix="metrics_fold", suffix=".json") -> dict:
        """
        Extracts a dictonary of metrics from spacy json file of metrics.

        Parameters
        ----------
        prefix : string
            start of name for each json file, going up to fold number
        suffix : string
            end of name for each json file, starting after fold number

        Returns dictonary of metrics.
        """
        metrics = defaultdict(list)
        for i in range(0, self.k_folds):
            file_name = prefix + str(i) + suffix
            json_dict = json_2_dict(file_name)
            for tag in self.tags:
                if tag in json_dict["ents_per_type"].keys():
                    data = json_dict["ents_per_type"][tag]
                    metrics[tag].append(data)
        return metrics

    def average_metrics(self, metrics : dict) -> dict:
        """
        Averages across folds metrics for each label as well as overall.

        Parameters
        ----------
        metrics : dict
            dictonary of metrics extracted from spacy json

        Returns dictonary of averages.
        """
        avg_metrics = {}
        p_all = []
        r_all = []
        f_all = []
        for k,v in metrics.items():
            p_temp = []
            r_temp = []
            f_temp = []
            for i in v:
                p_all.append(i.get("p"))
                r_all.append(i.get("r"))
                f_all.append(i.get("f"))

                p_temp.append(i.get("p"))
                r_temp.append(i.get("r"))
                f_temp.append(i.get("f"))
                avg_metrics[k] = [sum(p_temp)/len(p_temp), sum(r_temp)/len(r_temp), sum(f_temp)/len(f_temp)]
            avg_metrics["ALL"] = [sum(p_all)/len(p_all), sum(r_all)/len(r_all), sum(f_all)/len(f_all)]
        return avg_metrics

    def format_metrics(self, metrics : dict):
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
        for k,v in metrics.items():
            if k != "ALL":
                print(k+":")
                print("\t precision: " + str(metrics[k][0]))
                print("\t recall: " + str(metrics[k][1]))
                print("\t F1: " + str(metrics[k][2]))

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
            '--pos_tagging',
            action='store_true',
            help='do pos tagging after model training'
    )
    args = parser.parse_args()

    val = CrossValidation(k_folds=int(args.folds))
    val.cross_validate(args.dataset_dir, args.pos_tagging)
    if args.pos_tagging is False:
        avgs = val.average_metrics(val.extract_metrics())
        val.format_metrics(avgs)
