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
from json2SpacyJson import convertJsonToSpacyJsonl
from json2py import json_2_dict
from dataset2bratt import dataset_to_bratt
from validation_testing import execute




class Train_Test:

    def create_config(self, name="senter_ner.cfg", model_name="train_test_model", gpu=False, word_embed=False, vectors=
    "glove.6B.zip") -> str:
        """
        Creates spacy model config file

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
            execute("python3 -m spacy init config --lang en --pipeline transformer,senter,ner  --optimize accuracy --force " + name +" -G")
        elif self.spancat:
            execute("python3 -m spacy init config --lang en --pipeline tok2vec,senter,spancat  --optimize accuracy --force " + name)
        else:
            if word_embed:
                execute("python3 -m spacy init vectors en " + vectors + " "+ model_name)
            execute("python3 -m spacy init config --lang en --pipeline tok2vec,senter,ner  --optimize accuracy --force " + name)
        return name

    def train_test(self, data : str, config : str, model_name="train_test_model"):
        """
        Preforms cross validation on spacy model.

        Parameters
        ----------
        data : str
            path to data directort
        config : str
            path to model config file
        model_name : str
            start of output path for the model, each fold creates a model with
            that prefix and the suffix of _XFold where X is the fold number
        """
        # shuffles and divides data into k folds and a dev set
        print("\nShuffling and splitting data...")
        files = glob.glob(data+"/**/*.json", recursive=True)
        file_count = len(files)
        random.shuffle(files)
        training = files[0:file_count*.8]
        dev = files[file_count*.8:file_count*.9]
        validation = files [file_count*.9:file_count]

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
            execute("python src/add_ents_to_spans_dict.py ner_2021_08/ner_2021_08_dev_data.spacy en ner")


        # convert training data into spacy json and then into spacy binary
        print("\nConverting training data...")
        print("____________________________")
        convertJsonToSpacyJsonl(outputFileName="ner_2021_08_training_data.jsonl", filePaths=training)
        convert(input_path="ner_2021_08_training_data.jsonl", output_dir="ner_2021_08", converter="json", file_type="spacy")
        if self.spancat:
            execute("python src/add_ents_to_spans_dict.py ner_2021_08/ner_2021_08_training_data.spacy en ner")

        fold_dir, gold_bratt_dir = self.create_gold_dataset(validation)

        train(config_path=config, output_path=model_name, overrides={"paths.train": "ner_2021_08/ner_2021_08_training_data.spacy", "paths.dev": "ner_2021_08/ner_2021_08_dev_data.spacy"})


        # average metrics and print
        print("\nEvaluating with spacy only...")
        print("____________________________")
        self.predict("spacy", gold_bratt_dir, model_name+"/model-best")
        spacy_results = measure_dataset(Dataset("gold_bratt"), Dataset("spacy/pred_bratt"), 'strict')
        spacy_avg_metrics, spacy_ents_found, spacy_ent_counts = self.medacy_eval("spacy")
        print("Spacy only results")
        print("____________________________")
        self.print_metrics(spacy_avg_metrics, spacy_ents_found, spacy_ent_counts)
        print()

        if self.pos:
            print("\nEvaluating with spacy & pos...")
            print("____________________________")
            self.predict("pos", gold_bratt_dir, model_name+"/model-best")
            pos_results = measure_dataset(Dataset("gold_bratt"), Dataset("pos/pred_bratt"), 'strict')
            print("Spacy & POS tagging entity expansion results")
            print("____________________________")
            pos_avg_metrics, pos_ents_found, pos_ent_counts = self.medacy_eval("pos")
            self.print_metrics(pos_avg_metrics, pos_ents_found, pos_ent_counts)

    def predict(self, sub_dir : str, gold_dir : str, model_dir : str):
        """
        For a given fold, predicts on the validation data and saves to json.
        Also moves the gold standard validation data in json format to a new
        directory. Then converts both of these datasets to bratt format.

        Parameters
        ----------
        sub_dir : str
            path to subdirectory for output, either "pos" or "spacy"
        gold_dir : str
            path to gold standard dataset
        model_dir : str
            path to model
        """
        # create output directories
        print("\nCreating output directories...")
        json_name = sub_dir + "/pred_json"
        bratt_name =  sub_dir + "/pred_bratt"
        self.create_dirs([json_name, bratt_name])

        if sub_dir == "spacy":
            flag = True
        else:
            flag = False

        print("Predicting on validation data ...")
        print("____________________________")
        predict = Predict(model_dir=model_dir, dataset_dir=gold_dir, output_dir=json_name, spacy_only=flag)
        predict.process_files()

        # convert predictions to bratt format
        print("\nConverting predictions to bratt...")
        print("____________________________")
        dataset_to_bratt(input_dir=json_name, output_dir=bratt_name)

    def medacy_eval(self, sub_dir):
        """
        Finds average metrics and entity counts across all folds.
        Uses medacy's inter_dataset_agreement calculator to get
        precesion, recall, and f-score for each label and overall for each fold.
        Then finds averages of those metrics across every folds. Also keeps
        track of found entity counts and entitiy counts from gold standard.

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

        # inter_dataset_agreement for each fold
        ents_found["ALL"] = 0
        result = measure_dataset(Dataset("gold_bratt"), Dataset(sub_dir+"/pred_bratt"), 'strict')
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


        return avg_metrics, ents_found, ent_counts


    def create_gold_dataset(self, validation : list):
        """
        Creates gold standard dataset for current fold and converts to bratt.

        Parameters
        ----------
        validation : list
            list of file names to use for validation
        fold : int
            current fold, used for directory naming

        Returns name of directory for current fold and name of directory for
        bratt format gold standard data for this fold.
        """
        gold_json_name = "gold_json"
        gold_bratt_name = "gold_bratt"
        self.create_dirs([gold_json_name, gold_bratt_name])
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
