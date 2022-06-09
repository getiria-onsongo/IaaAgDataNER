# experimenting with navigating training json files to get pos tags
from json2py import *
from collections import defaultdict
import json

def load_jsonl(file_name):
    jsonl_as_list = json_2_dict(file_name)
    jsonl_dict = dict() # id mapped to full jsonl entry
    sen_dict = dict() # raw sentence mapped to token dict
    for entry in jsonl_as_list:
        sen_dict[entry['paragraphs'][0]['raw']] = entry['paragraphs'][0]['sentences'][0]['tokens']
    return sen_dict


def extract_pos(sen_dict):
    pos_dict = defaultdict() # raw sentence mapped to token dict just containing pos
    for sen_toks in sen_dict.keys():
        pos_dict[sen_toks] = defaultdict()
        for tok in sen_dict[sen_toks]:
            pos_dict[sen_toks][tok['orth']] = tok['pos']
    return pos_dict


def sentence_to_pos(raw_sen):
    return pos_dict[raw_sen]

# example
sen_dict = load_jsonl("ner_2021_08_training_data.jsonl")
pos_dict = extract_pos(sen_dict)
sen_to_pos = sentence_to_pos('COLTER  Colter is a six-rowed spring feed and malting barley.')
print(sen_to_pos['malting'])
