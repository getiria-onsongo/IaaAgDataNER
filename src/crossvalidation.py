from json2SpacyJson import convertJsonToSpacyJsonl
from spacy.cli.train import train
from spacy.cli.convert import convert
from spacy.cli.evaluate import evaluate
from agParse import *
import glob
import os
import random


def cross_validate(fold_number, data, pos_split):
    # shuffles and divides data into k folds and a dev set
    splits = fold_number + 1
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
    if not os.path.exists("ner_2021_08"):
        os.makedirs("ner_2021_08")

    # create and convert dev set
    dev = folds[len(folds)-1]
    convertJsonToSpacyJsonl(outputFileName="ner_2021_08_dev_data.jsonl", filePaths=dev)
    convert(converter="json", input_path="ner_2021_08_dev_data.jsonl", output_dir="ner_2021_08")

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
        convert(converter="json", input_path="ner_2021_08_training_data.jsonl", output_dir="ner_2021_08")
        convert(converter="json", input_path="ner_2021_08_validate_data.jsonl", output_dir="ner_2021_08")

        # train model
        train(config_path="senter_ner.cfg", output_path="ner_2021_08_model", overrides={"paths.train": "ner_2021_08/ner_2021_08_training_data.spacy", "paths.dev": "ner_2021_08/ner_2021_08_validate_data.spacy"})

        # evaulate model
        output_name = "output_metrics_fold" + str(v) + ".json"
        evaluate(model="ner_2021_08_model/model-best", data_path="ner_2021_08/ner_2021_08_dev_data.spacy", output=output_name)

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
