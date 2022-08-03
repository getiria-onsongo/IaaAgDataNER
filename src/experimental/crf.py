import glob
import json
from collections import defaultdict
import srsly
import spacy
from spacy.language import Language
from spacy_crfsuite.tokenizer import SpacyTokenizer
from spacy_crfsuite.train import gold_example_to_crf_tokens
from spacy_crfsuite import CRFExtractor
from spacy_crfsuite import CRFEntityExtractor
from cross_validation import CrossValidation
from inter_dataset_agreement import measure_dataset, format_results
from dataset2bratt import dataset_to_bratt
from json2py import json_2_dict
"""
Unfinished crf class
"""


@Language.factory("ner-crf")
def crf_component(nlp, name):
    crf_extractor = CRFExtractor().from_disk("crf.pkl")
    return CRFEntityExtractor(nlp, crf_extractor=crf_extractor)

class CRF:
    def __init__(self):
        self.cv = CrossValidation()

    def format_dict(self, file):
        json = json_2_dict(file)
        crf_dict = defaultdict()
        text = list(json["sentences"].keys())[0]
        crf_dict["text"] = text
        crf_dict["entities"] = []
        for s in json["sentences"].values():
            for e in s.values():
                start =  e["start"]
                end = e["end"]
                crf_dict["entities"].append({"start": start, "end": end, "value" : text[start:end], "entity":e["label"]})
        return crf_dict

    def create_gold_standard(self, validation, gold_json_name="gold_standard/json", gold_brat_name="gold_standard/brat" ):
        print("Creating gold standard dataset...")
        print("____________________________")
        self.cv.create_dirs([gold_json_name, gold_brat_name])
        for file in validation:
            json_file = open(file)
            contents = json.load(json_file)
            name_split = file.split("/")
            file_name = name_split[len(name_split)-1]
            with open(gold_json_name+"/"+file_name, 'w') as f:
                json.dump(contents, f)
            dataset_to_bratt(input_dir=gold_json_name, output_dir=gold_brat_name)
        return gold_brat_name

    def get_data(self, data_dir):
        data = glob.glob(data_dir+"/**/*.json", recursive=True)
        print(data)
        train = data[0:round(len(data)*.80)]
        print(len(train))
        val = data[round(len(data)*.80):len(data)]
        print(len(val))
        return train, val

    def train_crf(self, train, config):
        print("Formating dictonary...")
        print("____________________________")
        formated_train = []
        for f in train:
            formated_train.append(dict(self.format_dict(f)))
        print("Training...")
        print("____________________________")
        nlp = spacy.load("en_core_web_lg", disable=["ner"])
        tokenizer = SpacyTokenizer(nlp)
        train_dataset = [gold_example_to_crf_tokens(ex, tokenizer=tokenizer) for ex in formated_train]
        component_config = srsly.read_json(config)
        crf_extractor = CRFExtractor(component_config=component_config)
        rs = crf_extractor.fine_tune(train_dataset, cv=5, n_iter=50, random_state=42)
        print("best_params:", rs.best_params_, ", score:", rs.best_score_)
        crf_extractor.train(train_dataset)
        print("Evaluating crf...")
        print("____________________________")
        classification_report = crf_extractor.eval(train_dataset)
        print(classification_report[1])
        crf_extractor.to_disk("crf.pkl")

    def medacy_eval(self, gold, system):
        print("Evaluating model...")
        print("____________________________")
        results = measure_dataset(gold, system)
        format_results(results)

    def predict(self, gold_dir, model_name="crf_model", json_output_name="predictions/crf_json", brat_output_name="predictions/crf_brat"):
        print("Predicting...")
        print("____________________________")
        self.cv.create_dirs([json_output_name, brat_output_name])
        nlp = spacy.load("en_core_web_lg", disable=["ner"])
        nlp.add_pipe("ner-crf")
        nlp.to_disk(model_name)
        predict = Predict(model_dir=model_name, dataset_dir=gold_dir, output_dir=json_output_name)
        predict.process_files()
        dataset_to_bratt(input_dir=json_output_name, output_dir=brat_output_name)
        return brat_output_name

crf = CRF()
train, val = crf.get_data("../../Data/IaaAgDataNER/dev_onsongo")
# train, val = crf.get_data("Data/dev_onsongo")
# gold = crf.create_gold_standard(val)
crf.train_crf(train, "../crf_config.json")
crf.train_crf(train, "crf_config.json")
system = crf.predict(gold_dir=gold)
crf.medacy_eval(gold, system)
