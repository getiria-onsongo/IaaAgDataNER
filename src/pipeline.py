
from agParse import *
from tkinterColorList import  *
from datetime import datetime
from functools import partial
from json2py import *
import os.path
from py2json import *
import PyPDF2
import re
import random
import tkinter as tk
from tkinter import filedialog as fd
from collections import defaultdict
from tkinter.scrolledtext import ScrolledText
import os
import sys

# only works with a single line of text
# need to multiline tagging & inputing whole files & dirs

class Pipeline:

    def __init__(self, model_dir, text):
        self.model_dir = model_dir
        self.nlp = None
        self.cust_ents_dict = {}
        self.text = text
        self.tags=["highlight","default_color_tag","ALAS","CROP","CVAR","JRNL","PATH","PED","PLAN","PPTD","TRAT"]
        self.nlp_pos = spacy.load("en_core_web_lg") # spacy model to use for pos
        self.crop_cnt = {}
        self.cvar_cnt = {}


    def load_model(self):
        self.nlp = spacy.load(self.model_dir)
        self.nlp.add_pipe("compound_trait_entities", after='ner')


    def get_pos(self, ent, nlp):
        '''
        Proceses a given entity with rules that use pos tag data to expand the entity span if needed.

        :param ent: entity to possibly expand span of
        :param nlp: spacy model for pos tagging
        :returns: entity, with an expanded span if needed
        '''
        doc = nlp(ent.sent.text)
        if(len(doc[ent.start:ent.end]) > 0):
            current_index = doc[ent.start:ent.end][0].i
            label = ent.label_
            # functions that contain rules to expand the entity's span
            ent = self.adj_combine_noun_ent(doc, current_index, ent, label)
            ent = self.num_combine_ent(doc, current_index, ent, label)
        return ent


    def adj_combine_noun_ent(self, doc, current_index, ent, label):
        '''
        If the first token in an entity is a noun or proper noun, finds all adjectives proceeding the entity and expands the span to contain all of them.

        :param doc: sentence entity belongs to passed through spacy model
        :param current_index: index of first token in the doc
        :param ent: entity to possibly expand span of
        :param label: label of ent
        :returns: entity, which has been expanded if needed
        '''
        if current_index >= 1:
            current = doc[current_index]
            left = doc[current_index-1]
            pos_current = current.pos_
            pos_left = left.pos_

            if pos_current == "NOUN" or pos_current == "PROPN":
                if pos_left == "ADJ":
                        print("Adj expanding...")
                        print("entity: "+ str(ent))
                        i = current_index
                        start_index = ent.start
                        # keeps searching until all adjectives are found, for nouns described by mutiple entities
                        while i >= 1:
                            i = i - 1
                            if doc[i].pos_ == "ADJ":
                                start_index = i
                            else:
                                break
                        first_tok = doc[start_index]
                        ent = doc[first_tok.i:ent.end]
                        ent.label_ = label
                        print("new: " + str(ent))
                        print("label: " + str(ent.label_))
                        print()
        return ent


    def num_combine_ent(self, doc, current_index, ent, label):
        '''
        If the first token in an entity is a noun, proper noun, or adjective, finds expands the span to include a numerical measurment that comes before the entity. The measurment is found by seeing if it conforms to the format num-noun-entity. So, "30 mg wheat" would be fulfill the rule but "12 wheat" would not.

        :param doc: sentence entity belongs to passed through spacy model
        :param current_index: index of first token in the doc
        :param ent: entity to possibly expand span of
        :param label: label of ent
        :returns: entity, which has been expanded if needed
        '''
        if current_index >= 2:
            current = doc[current_index]
            left = doc[current_index-1]
            left_left = doc[current_index-2]
            pos_current = current.pos_
            pos_left = left.pos_
            pos_left_left = left_left.pos_
            if pos_current == "ADJ" or pos_current == "NOUN" or pos_current == "PROPN" :
                if pos_left == "PROPN" or pos_left == "NOUN":
                    if pos_left_left == "NUM":
                        print("Num expanding...")
                        print("entity: " + str(ent))
                        ent = doc[left_left.i:ent.end]
                        ent.label_ = label
                        print("new: " + str(ent))
                        print("label: " + str(ent.label_))
                        print()
        return ent

    def tag(self):
        """ Pre-tag selected content or all the text in text box with NER tags. """
        # Reset annotation dictionary
        self.cust_ents_dict = {}
        input_text = self.text
        doc = self.tag_ner_with_spacy(input_text)
        for ent in doc.ents:
            if (ent.label_ in self.tags):
                # does pos tagging and expaning the ent span if needed
                ent = self.get_pos(ent, self.nlp_pos)
                # Add tag to crop or cvar if it is one of the two.
                ent_value = input_text[ent.start_char:ent.end_char].strip().lower()
                if(ent.label_ == 'CROP'):
                    self.add_to_dict(self.crop_cnt,ent_value)
                if (ent.label_ == 'CVAR'):
                    self.add_to_dict(self.cvar_cnt, ent_value)
                lineNo = 1 # hot fix
                if (self.cust_ents_dict.get(lineNo, False)):
                    self.cust_ents_dict[lineNo].append((ent.start_char, ent.end_char, ent.label_))
                else:
                    self.cust_ents_dict[lineNo] = [(ent.start_char, ent.end_char, ent.label_)]

        if (self.cust_ents_dict.get(lineNo, False)):
                tags = self.cust_ents_dict[lineNo]
                self.cust_ents_dict[lineNo] = [input_text,tags]



    def tag_ner_with_spacy(self, text):
        """ Use SpaCy to identify NER in text"""
        doc = self.nlp(text)
        return doc


    def add_to_dict(self, dictionary, ent_value):
        """ Add documentation"""
        if (dictionary.get(ent_value, False)):
            dictionary[ent_value] = dictionary[ent_value] + 1
        else:
            dictionary[ent_value] = 1


if __name__ == '__main__':
    pipeline = Pipeline("senter_ner_2021_08_model/model-best", 'CV-133, PI 653260) hard red winter wheat (Triticum aestivum L.) was')
    pipeline.load_model()
    pipeline.tag()
    print(pipeline.cust_ents_dict)
