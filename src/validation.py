
from agParse import *
from functools import partial
from json2py import *
import os.path
from py2json import *
import PyPDF2
import re
import random
from collections import defaultdict
import os
import sys
import glob
from conversions import conversion

# only works with a single line of text
# need to multiline tagging & inputing whole files & dirs

class Pipeline:

    def __init__(self, file_dir, model_dir, spacy_model_name="en_core_web_lg", tags=["ALAS","CROP","CVAR","JRNL","PATH","PED","PLAN","PPTD","TRAT"]):
        self.file_dir = file_dir
        self.model_dir = model_dir
        self.spacy_model_name = spacy_model_name # spacy model to use for pos
        self.tags = tags
        self.nlp_pos = spacy.load(self.spacy_model_name)
        self.nlp = None
        self.cust_ents_dict = {}
        self.crop_cnt = {}
        self.cvar_cnt = {}
        self.page_num = 0

    def load_model(self):
        self.nlp = spacy.load(self.model_dir)
        self.nlp.add_pipe("compound_trait_entities", after='ner')

    def process_files(self):
        """
        Gets the directory of pdfs, reads them in and then does ner tagging on them,
        saves as json, and then converts and saves them as bratt files. May need a
        feature to make sure train/test split is maintained. Need to switch to working
        at page level (issue with pdf reader).
        """
        files = glob.glob("Data/CSU/*.pdf")
        print(files)
        for f in files:
            pdf_file = open(f, mode="rb")
            pdfReader = PyPDF2.PdfFileReader(pdf_file)
            page_count = len(pdfReader.pages)
            page_num = 0
            while page_num <= page_count:
                page = pdfReader.getPage(page_num - 1)
                page_text = page.extractText()
                page_text = re.sub('\n', '', page_text)
                page_text = re.sub('\.\s', '.\n', page_text)
                page_text = re.sub('\s\s', '\n', page_text)
                self.tag(page_text)
                json_name = self.file_save(f, "", page_num)
                bratt_name = f[0:len(f)-4] + "_p" + str(page_num) + "_td_out.ann"
                conversion(json_name, bratt_name)
                page_num = page_num + 1
            pdf_file.close()


    def tag(self, text):
        """ Pre-tag selected content or all the text in text box with NER tags. """
        # Reset dictionaries
        self.cust_ents_dict = {}
        self.crop_cnt = {}
        self.cvar_cnt = {}
        lineNo = 0
        sents = self.get_sents(text, self.nlp_pos)
        for sent in sents:
            lineNo = lineNo + 1
            doc = self.tag_ner_with_spacy(sent.text)
            for ent in doc.ents:
                if (ent.label_ in self.tags):
                    # does pos tagging and expaning the ent span if needed
                    ent = self.get_pos(ent, self.nlp_pos)
                    # Add tag to crop or cvar if it is one of the two.
                    ent_value = text[ent.start_char:ent.end_char].strip().lower()
                    if(ent.label_ == 'CROP'):
                        self.add_to_dict(self.crop_cnt,ent_value)
                    if (ent.label_ == 'CVAR'):
                        self.add_to_dict(self.cvar_cnt, ent_value)
                    if (self.cust_ents_dict.get(lineNo, False)):
                        self.cust_ents_dict[lineNo].append((ent.start_char, ent.end_char, ent.label_))
                    else:
                        self.cust_ents_dict[lineNo] = [(ent.start_char, ent.end_char, ent.label_)]

            if (self.cust_ents_dict.get(lineNo, False)):
                tags = self.cust_ents_dict[lineNo]
                self.cust_ents_dict[lineNo] = [text,tags]


    def get_sents(self, text, nlp):
        """
        likley can remove this soon, just to get line counts / numbers.
        """
        doc = self.nlp_pos(text)
        return doc.sents

    def tag_ner_with_spacy(self, text):
        """ Use SpaCy to identify NER in text"""
        doc = self.nlp(text)
        return doc

    def get_pos(self, ent, nlp):
        """
        Proceses a given entity with rules that use pos tag data to expand the entity span if needed.

        :param ent: entity to possibly expand span of
        :param nlp: spacy model for pos tagging
        :returns: entity, with an expanded span if needed
        """
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


    def add_to_dict(self, dictionary, ent_value):
        """ Add documentation"""
        if (dictionary.get(ent_value, False)):
            dictionary[ent_value] = dictionary[ent_value] + 1
        else:
            dictionary[ent_value] = 1


    def file_save(self, name, url, chunk):
        """ Simplifed version of GUI save file. """"
        crop = str(self.get_max_dict_value(self.crop_cnt))
        cvar = str(self.get_max_dict_value(self.cvar_cnt))
        name_prefix = name[0:len(name)-4]
        output_filename = name_prefix + "_p" + str(chunk) + "_td_out.json"
        train_data = []
        for lineNo in self.cust_ents_dict:
            text_ents = self.cust_ents_dict[lineNo]
            text_value = text_ents[0].strip()
            ents_value = text_ents[1]
            ents_value.sort()
            ents = {'entities': ents_value}
            train_data.append((text_value, ents))
        train_dict = mixed_type_2_dict(train_data, chunk, name, url, crop, cvar)
        dict_2_json(train_dict, output_filename)
        print("saved file")
        return output_filename


    def get_max_dict_value(self, dictionary):
        """ Add documentation"""
        maxKey = None
        maxValue = 0
        for key, value in dictionary.items():
            if value > maxValue:
                maxKey = key
                maxValue = value
        return maxKey


if __name__ == '__main__':
    pipeline = Pipeline("Data/UIdaho2019", "senter_ner_2021_08_model/model-best")
    pipeline.load_model()
    pipeline.load_files()
