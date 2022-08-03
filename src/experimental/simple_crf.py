from collections import defaultdict
import spacy
import srsly
from spacy.language import Language
from spacy_crfsuite import read_file
from spacy_crfsuite.tokenizer import SpacyTokenizer
from spacy_crfsuite.train import gold_example_to_crf_tokens
from spacy_crfsuite import CRFExtractor
from spacy_crfsuite import CRFEntityExtractor
from json2py import json_2_dict
"""
Old version of stripped down crf class, now rewritten in crf.py, but
smaller and therefore useful to keep around.

"""

class SimpleCRF():

    def __init__(self, nlp, paths):
        self.train_crf(nlp, paths)

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

    def train_crf(self, nlp, paths):
        train_data = []
        for f in paths:
            train_data.append(dict(self.format_dict(f)))

        tokenizer = SpacyTokenizer(nlp)
        train_dataset = [gold_example_to_crf_tokens(ex, tokenizer=tokenizer) for ex in train_data]
        component_config = srsly.read_json("../crf_config.json")
        crf_extractor = CRFExtractor(component_config=component_config)
        rs = crf_extractor.fine_tune(train_dataset, cv=5, n_iter=50, random_state=42)
        print("best_params:", rs.best_params_, ", score:", rs.best_score_)
        crf_extractor.train(train_dataset)
        classification_report = crf_extractor.eval(train_dataset)
        print(classification_report[1])
        crf_extractor.to_disk("model.pkl")



# paths = ["../../Data/IaaAgDataNER/dev_onsongo/barley_p10_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p10_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p11_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p12_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p13_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p14_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p15_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p16_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p17_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p18_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p19_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p20_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p21_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p22_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p23_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p24_td.json", "../../Data/IaaAgDataNER/dev_onsongo/barley_p25_td.json"]
#
# nlp = spacy.load("en_core_web_sm", disable=["ner"])
# crf = SpacyCRF(nlp, paths)
# nlp.add_pipe("ner-crf")
