from json2SpacyJson import convertJsonToSpacyJsonl
from validation_testing import execute
from spacy.cli.train import train
from spacy.cli.convert import convert
import glob
import os
from agParse import *
import random


def cross_validate(fold_number, data, pos_split):
    # shuffles and divides data into k folds and a dev set
    files = glob.glob(data+"/*.json") # add feature to search multiple dirs?
    random.shuffle(files)
    files_per_divison = (len(files) // fold_number) + 2 # should I round up or down?
    folds = []
    start,end = 0,1
    for i in range(0, fold_number):
        if i != files_per_fold:
            folds.append(files[files_per_divison*start:files_per_divison*end])
            start += 1
            end += 1
        else:
            folds.append(files[files_per_divison*start:len(files)])

    # makes spacy binary output dir if it doesn't exist
    if not os.path.exists("ner_2021_08"):
        os.makedirs("ner_2021_08")

    # create and convert dev set
    dev = folds[fold_number]
    convertJsonToSpacyJsonl(outputFileName="ner_2021_08_dev_data.jsonl", filePaths=dev)
    convert(input_path="ner_2021_08_dev_data.jsonl", output_dir="ner_2021_08")

    # k-fold cross validation
    for v in range(0, fold_number):
        # train - validate split
        training = []
        for t in range(0, fold_number):
            if t != v:
                training += folds[t]
        validation = folds[v]

        # json to spacy json
        convertJsonToSpacyJsonl(outputFileName="ner_2021_08_training_data.jsonl", filePaths=training)
        convertJsonToSpacyJsonl(outputFileName="ner_2021_08_validate_data.jsonl", filePaths=validation)

        # spacy json to spacy binary
        convert(input_path="ner_2021_08_training_data.jsonl", output_dir="ner_2021_08")
        convert(input_path="ner_2021_08_validate_data.jsonl", output_dir="ner_2021_08")

        # train model
        train(config_path="../senter_ner.cfg", output_path="ner_2021_08_model", overrides={"paths.train": "ner_2021_08/ner_2021_08_training_data.spacy", "paths.dev": "ner_2021_08/ner_2021_08_validate_data.spacy"})

        # evaulate model
        out_metrics_path = "metrics_fold_" + str(v) + "_.json"
        evaluate(model="ner_2021_08_model", data_path="ner_2021_08/ner_2021_08_dev_data.spacy", output_path=out_metrics_path)

        if pos_split:
            print("Not implemented.")


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
    cross_validate(int(args.folds), args.dataset_dir, args.pos_tagging)
