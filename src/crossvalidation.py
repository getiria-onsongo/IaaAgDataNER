from sklearn.model_selection import KFold
from json2SpacyJson import convertJsonToSpacyJsonl
from validation_testing import execute
import glob
import os
import random

def cross_validate(fold_number, data, pos_split):
    # divide data into folds
    files = glob.glob(data+"/*.json") # add feature to search multiple dirs?
    random.shuffle(files)
    files_per_fold = (len(files) // fold_number) + 1 # should I round up or down?
    folds = []
    start,end = 0,1
    for i in range(0, fold_number):
        if i != files_per_fold:
            folds.append(files[files_per_fold*start:files_per_fold*end])
            start += 1
            end += 1
        else:
            folds.append(files[files_per_fold*start:len(files)])

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
        if not os.path.exists("ner_2021_08"):
            os.makedirs("ner_2021_08")
        execute("python3 -m spacy convert --converter json ner_2021_08_training_data.jsonl ner_2021_08")
        execute("python3 -m spacy convert --converter json ner_2021_08_validate_data.jsonl ner_2021_08")

        # train model
        execute("python3 -m spacy train senter_ner.cfg --output ner_2021_08_model --paths.train ner_2021_08/ner_2021_08_training_data.spacy --paths.dev ner_2021_08/ner_2021_08_validate_data.spacy")

        if pos_split:
            pass
            # pos post-processing here



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
    cross_validate(args.folds, args.dataset_dir, args.pos_tagging)
