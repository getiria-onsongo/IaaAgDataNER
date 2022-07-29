from collections import defaultdict
import spacy
import srsly
from spacy_crfsuite import read_file
from spacy_crfsuite.tokenizer import SpacyTokenizer
from spacy_crfsuite.train import gold_example_to_crf_tokens
from spacy_crfsuite import CRFExtractor
from spacy_crfsuite import CRFEntityExtractor
from json2py import json_2_dict

def format_dict(f):
    json = json_2_dict(f)
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

def create_crf_component(paths):
    train_data = []
    for f in paths:
        train_data.append(dict(format_dict(f)))

    nlp = spacy.load("en_core_web_sm", disable=["ner"])
    tokenizer = SpacyTokenizer(nlp)
    train_dataset = [gold_example_to_crf_tokens(ex, tokenizer=tokenizer) for ex in train_data]
    component_config = srsly.read_json("../crf_config.json")
    crf_extractor = CRFExtractor(component_config=component_config)
    rs = crf_extractor.fine_tune(train_dataset, cv=5, n_iter=50, random_state=42)
    print("best_params:", rs.best_params_, ", score:", rs.best_score_)
    crf_extractor.train(train_dataset)
    classification_report = crf_extractor.eval(train_dataset)
    print(classification_report[1])
    return CRFEntityExtractor(nlp, crf_extractor=crf_extractor)
