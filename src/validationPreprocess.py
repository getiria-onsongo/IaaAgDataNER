import os.path
from datetime import datetime
import re
import glob
from pyxpdf import Document, Page, Config
from pyxpdf.xpdf import TextControl
from jsontobratt import conversion
from datasettobratt import dataset_to_bratt
from agParse import *
from json2py import *
from py2json import *


class ValidationPreprocess:

    def __init__(self, file_dir, model_dir, output_dir="Data/Output/", spacy_model_name="en_core_web_lg", tags=["ALAS","CROP","CVAR","JRNL","PATH","PED","PLAN","PPTD","TRAT"]):
        self.file_dir = file_dir
        self.model_dir = model_dir
        self.output_dir = output_dir
        self.spacy_model_name = spacy_model_name # spacy model to use for pos
        self.nlp_pos = spacy.load(self.spacy_model_name)
        self.nlp =  spacy.load(self.model_dir)
        self.nlp.add_pipe("compound_trait_entities", after='ner')
        self.cust_ents_dict = {}
        self.crop_cnt = {}
        self.cvar_cnt = {}
        self.page_num = 0
        self.tags = tags


    def process_files(self, file_ending="/*.pdf"):
        """
        Gets the directory of pdfs, reads them in and then does ner tagging on them,
        saves as json, and then converts and saves them as bratt files. May need a
        feature to make sure train/test split is maintained. Need to switch to working
        at page level (issue with pdf reader).
        """
        files = glob.glob(self.file_dir+file_ending)
        print("%s files to process." %str(len(files)))
        for f in files:
            self.cust_ents_dict = {}
            pdf_document = Document(f)
            page_number = 1
            while page_number <= len(pdf_document):
                self.tag(pdf_document, page_number)
                json_name = self.file_save(f, "", page_number)
                bratt_name = json_name[0:len(json_name)-5]
                conversion(json_name, bratt_name)
                page_number = page_number + 1




    def tag(self, pdf_document, page_number):
        """ Pre-tag selected content or all the text in text box with NER tags. """
        self.cust_ents_dict = {}
        control = TextControl(mode="physical")
        page = pdf_document[page_number - 1]
        input_text = page.text(control=control)
        doc = self.nlp(input_text)

        for ent in doc.ents:
            if (ent.label_ in self.tags):
                ent = self.get_pos(ent, self.nlp_pos)
                if self.cust_ents_dict.get(page_number, False):
                    self.cust_ents_dict[page_number].append((ent.start_char, ent.end_char, ent.label_))
                else:
                    self.cust_ents_dict[page_number] = [(ent.start_char, ent.end_char, ent.label_)]
        if (self.cust_ents_dict.get(page_number, False)):
            tags = self.cust_ents_dict[page_number]
            self.cust_ents_dict[page_number] = [input_text, tags]


    def get_pos(self, ent, nlp_pos):
        """
        Proceses a given entity with rules that use pos tag data to expand the entity span if needed.

        :param ent: entity to possibly expand span of
        :param nlp: spacy model for pos tagging
        :returns: entity, with an expanded span if needed
        """
        doc = nlp_pos(ent.sent.text)
        if(len(doc[ent.start:ent.end]) > 0):
            current_index = doc[ent.start:ent.end][0].i
            label = ent.label_
            # functions that contain rules to expand the entity's span
            ent = self.adj_combine_noun_ent(doc, current_index, ent, label)
            # ent = self.num_combine_ent(doc, current_index, ent, label)
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


    def file_save(self, pdf_name, url, chunk, name_prefix="barley", name_suffix="_td.json", copy=False):
        """ Simplifed version of GUI save file & continue_func. """
        if name_prefix == None:
            name_prefix = pdf_name.split(".")[0].split("/")[2]
        output_filename = self.output_dir + name_prefix + "_p" + str(chunk) + name_suffix

        if os.path.isfile(output_filename):
            if copy:
                print("Making file copy...")
                now = datetime.now()  # current date and time
                date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
                output_filename = self.output_dir + name_prefix  + "_" + datatime + "_" + name_suffix
            else:
                print("File will be overwritten.")

        if len(self.cust_ents_dict) == 0:
            print("No annotations to save.")
        else:
            input_text = self.cust_ents_dict[chunk][0]
            entities = self.cust_ents_dict[chunk][1]
            input_text = re.sub(' +', ' ', input_text)
            ann_train_dict = mixed_type_2_dict([(input_text,{'entities': entities})], chunk, pdf_name, url)
            dict_2_json(ann_train_dict, output_filename)
            print("Created %s." %output_filename)

        return output_filename


if __name__ == '__main__':
    dataset = "Data/DavisLJ11"
    model = "senter_ner_2021_08_model/model-best"
    # dataset_to_bratt(dataset, output_dir="Data/InputDavis/")
    preprocess = ValidationPreprocess(dataset, model, output_dir="Data/OutputDavis/")
    preprocess.process_files()
