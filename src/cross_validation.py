from json2SpacyJson import convertJsonToSpacyJsonl
from json2py import json_2_dict
from spacy.cli.convert import convert
from spacy.cli.train import train
from spacy.cli.evaluate import evaluate
from validation_testing import execute
from agParse import *
import glob
import os
import json
import random
from predict import Predict
from dataset2bratt import dataset_to_bratt

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
    extract_metrics(self, prefix="metrics_fold", suffix=".json")
        for json files created from spacy evaluation, extracts into dictionary
    average_metrics(self, metrics : dict)
        averages values across folds for dictonary created in extract_metrics
    format_metrics(self, metrics : dict)
        prints formated contents of dictonary created in average_metrics
    create_dirs(self, dirs : list[str])
        for a list of directories, checks if they exist and if not creates them
    """
    def __init__(self, k_folds=5, tags=["ALAS", "CROP", "CVAR", "PATH", "PED", "PLAN", "PPTD", "TRAT"]):
        self.k_folds = k_folds
        self.tags = tags

    def cross_validate(self, data, pos_split):
        # shuffles and divides data into k folds and a dev set
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
        print(folds)

        # makes spacy binary output dir if it doesn't exist
        self.create_dirs(["ner_2021_08"])

        # create and convert the dev set
        # this is used for every fold's spacy training & doesn't change
        dev = folds[len(folds)-1]
        convertJsonToSpacyJsonl(outputFileName="ner_2021_08_dev_data.jsonl", filePaths=dev)
        convert(input_path="ner_2021_08_dev_data.jsonl", output_dir="ner_2021_08", converter="json", file_type="spacy")

        # k-fold cross validation
        for v in range(0, self.k_folds):
            # train - validate split
            training = []
            for t in range(0, self.k_folds):
                if t != v:
                    training += folds[t]
            validation = folds[v]

            # convert training data into spacy json and then into spacy binary
            convertJsonToSpacyJsonl(outputFileName="ner_2021_08_training_data.jsonl", filePaths=training)
            convert(input_path="ner_2021_08_training_data.jsonl", output_dir="ner_2021_08", converter="json", file_type="spacy")

            # train model
            train(config_path="senter_ner.cfg", output_path="cv_2021_08_model", overrides={"paths.train": "ner_2021_08/ner_2021_08_training_data.spacy", "paths.dev": "ner_2021_08/ner_2021_08_dev_data.spacy"})

            # evaulate model
            if pos_split:
                # create needed directories
                json_name = "pos_cv_val_" + str(v) + "_json"
                bratt_name = "pos_cv_val_" + str(v) + "_bratt"
                gold_json_name = "pos_cv_val_" + str(v) + "_gold_json"
                gold_bratt_name = "pos_cv_val_" + str(v) + "_gold_bratt"
                self.create_dirs([json_name, bratt_name, gold_json_name, gold_bratt_name])

                # do pos tagging & entity expansion
                predict = Predict("cv_2021_08_model/model-best", json_name)
                predict.preprocess(validation)

                # create gold standard dataset and convert both to bratt
                # can now be run through medacy's inter_dataset_agreement tool for evaulation
                for file in validation:
                    json_file = open(file)
                    contents = json.load(json_file)
                    ls = file.split("/")
                    file_name = ls[len(ls)-1]
                    with open(gold_json_name+"/"+file_name, 'w') as f:
                        json.dump(contents, f)
                dataset_to_bratt(gold_json_name, gold_bratt_name)
                dataset_to_bratt(json_name, bratt_name)

            else:
                # convert validate data
                convertJsonToSpacyJsonl(outputFileName="ner_2021_08_validate_data.jsonl", filePaths=validation)
                convert(input_path="ner_2021_08_validate_data.jsonl", output_dir="ner_2021_08", converter="json", file_type="spacy")
                output_name = "metrics_fold" + str(v) + ".json"

                # evaluate
                evaluate(model="ner_2021_08_model/model-best", data_path="ner_2021_08/ner_2021_08_validate_data.spacy", output=output_name)

    def extract_metrics(self, prefix="metrics_fold", suffix=".json"):
        metrics = defaultdict(list)
        for i in range(0, self.k_folds):
            file_name = prefix + str(i) + suffix
            json_dict = json_2_dict(file_name)
            for tag in self.tags:
                data = json_dict["ents_per_type"][tag]
                metrics[tag].append(data)
        return metrics

    def average_metrics(self, metrics):
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

    def format_metrics(self, metrics):
        print("ALL:")
        print("\t precesion: " + str(metrics["ALL"][0]))
        print("\t recall: " +  str(metrics["ALL"][1]))
        print("\t F1: " +  str(metrics["ALL"][2]))
        for k,v in metrics.items():
            if k != "ALL":
                print(k+":")
                print("\t precesion: " + str(metrics[k][0]))
                print("\t recall: " + str(metrics[k][1]))
                print("\t F1: " + str(metrics[k][2]))

    def create_dirs(self, dirs):
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
            action='store_true', default=False,
            help='do pos tagging after model training'
    )
    args = parser.parse_args()

    val = CrossValidation(k_folds=int(args.folds))
    val.cross_validate(args.dataset_dir, args.pos_tagging)
    avgs = val.average_metrics(val.extract_metrics())
    val.format_metrics(avgs)
