import os.path
from datetime import datetime
import re
import glob
from pyxpdf import Document
from pyxpdf.xpdf import TextControl
from json2bratt import conversion
from dataset2bratt import dataset_to_bratt
from agParse import *
from json2py import *
from py2json import *


class ValidationPreprocess:
    """ A class to prepare data for medacy validation

    ...
    Attributes
    ----------
    self.model_dir : str
        path to trained model for ner tagging
    self.dataset_dir : str
        path to dataset
    self.output_dir : str
        path to output files ran through model
    self.name_prefix : str
        start of file name for a new json file
    self.name_suffix : str
        end of json files, both from gold standard dataset and ones being created
    self.no_overwrite: bool
        flag for overwritting files or creating new ones
    self.spacy_model_name : str
        name of spacy model to use for pos
    self.pos_model : spacy.Language
        model to use for pos
    self.nlp : spacy.Language
        model to use for training
    self.tags : list[str]
        list of possible ner tags
    self.cust_ents_dict : dict
        keeps track of entities found
    self.crop_cnt : dict
        counts crop entities
    self.cvar_cnt : dict
        counts crop varient entities
    self.page_num : int
        current page number

    Methods
    -------
    process_files(self)
        process files by running through model then converting and saving
        json, bratt & txt of files
    tag(self, pdf_document : pyxpdf.Document, page_number : int)
        finds entities for a given page in a pdf
    get_pos(self, ent : str )
        finds the part of speech for an entity and expands if needed
    adj_combine_noun_ent(self, doc : spacy.Doc, current_index : int, ent :
    str, label : str)
        expands an entity to contain adjectives
    num_combine_ent(self, doc : spacy.Doc, current_index : int, ent : str,
    label : str)
        expands an entity to contain numerical measurments
    file_save(self, pdf_name : str, url : str, chunk : int)
        saves json for a file
    """

    def __init__(self, model_dir, dataset_dir, output_dir, name_prefix=None, name_suffix="td.json", no_overwrite=False, spacy_model_name="en_core_web_lg", tags=["ALAS", "CROP", "CVAR", "JRNL", "PATH", "PED", "PLAN", "PPTD", "TRAT"]):
        self.model_dir = model_dir
        self.dataset_dir = dataset_dir
        self.output_dir = output_dir

        self.name_prefix = name_prefix
        self.name_suffix = name_suffix
        self.no_overwrite = no_overwrite
        self.spacy_model_name = spacy_model_name  # spacy model to use for pos
        self.pos_model = spacy.load(self.spacy_model_name)
        self.nlp = spacy.load(self.model_dir)
        self.nlp.add_pipe("compound_trait_entities", after='ner')
        self.tags = tags

        self.cust_ents_dict = {}
        self.crop_cnt = {}
        self.cvar_cnt = {}
        self.page_num = 0

    def process_files(self):
        '''
        Gets the directory of pdfs, reads them in and then does ner tagging on them,
        saves as json, and then converts and saves them as bratt files. May need a
        feature to make sure train/test split is maintained.
        '''
        file_ending = "/*.pdf"
        files = glob.glob(self.dataset_dir+file_ending)
        print("%s files to process." % str(len(files)))
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
        '''
        Pre-tag selected content or all the text in text box with NER tags.

        Parameters
        ----------
        pdf_document : pyxpdf.Document
            pdf being processed
        page_number : int
            current page to tag
        '''
        self.cust_ents_dict = {}
        control = TextControl(mode="physical")
        page = pdf_document[page_number - 1]
        input_text = page.text(control=control)
        doc = self.nlp(input_text)

        for ent in doc.ents:
            if (ent.label_ in self.tags):
                ent = self.get_pos(ent)
                if self.cust_ents_dict.get(page_number, False):
                    self.cust_ents_dict[page_number].append(
                        (ent.start_char, ent.end_char, ent.label_))
                else:
                    self.cust_ents_dict[page_number] = [
                        (ent.start_char, ent.end_char, ent.label_)]
        if (self.cust_ents_dict.get(page_number, False)):
            tags = self.cust_ents_dict[page_number]
            self.cust_ents_dict[page_number] = [input_text, tags]

    def get_pos(self, ent):
        '''
        Proceses a given entity with rules that use pos tag data to expand
        the entity span if needed.

        Parameters
        ----------
        ent : str
            entity to possibly expand span of

        Returns expanded entity.
        '''
        doc = self.pos_model(ent.sent.text)
        if(len(doc[ent.start:ent.end]) > 0):
            current_index = doc[ent.start:ent.end][0].i
            label = ent.label_
            # functions that contain rules to expand the entity's span
            ent = self.adj_combine_noun_ent(doc, current_index, ent, label)
            # ent = self.num_combine_ent(doc, current_index, ent, label)
        return ent

    def adj_combine_noun_ent(self, doc, current_index, ent, label):
        '''
        If the first token in an entity is a noun or proper noun, finds all
        adjectives proceeding the entity and expands the span to contain
        all of them.

        Parameters
        ----------
        doc : spacy.Doc
            spacy model for pos with given sentence passed in
        current_index : int
            index of first token in the doc
        ent : str
            entity to possibly expand span of
        label : str
            label of ent

        Returns expanded entity.
        '''
        if current_index >= 1:
            current = doc[current_index]
            left = doc[current_index-1]
            pos_current = current.pos_
            pos_left = left.pos_

            if pos_current == "NOUN" or pos_current == "PROPN":
                if pos_left == "ADJ":
                    print("Adj expanding...")
                    print("entity: " + str(ent))
                    i = current_index
                    start_index = ent.start
                    # keeps searching until all adjectives are found
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
        If the first token in an entity is a noun, proper noun, or
        adjective,  expands the span to include a numerical measurment that
        comes before the entity. The measurment is found by seeing if it
        conforms to the format num-noun-entity. So, "30 mg wheat" would be
        fulfill the rule but "12 wheat" would not.

        Parameters
        ----------
        doc : spacy.Doc
            spacy model for pos with given sentence passed in
        current_index : int
            index of first token in the doc
        ent : str
            entity to possibly expand span of
        label : str
            label of ent

        Returns expanded entity.
        '''
        if current_index >= 2:
            current = doc[current_index]
            left = doc[current_index-1]
            left_left = doc[current_index-2]
            pos_current = current.pos_
            pos_left = left.pos_
            pos_left_left = left_left.pos_
            if pos_current == "ADJ" or pos_current == "NOUN" or pos_current == "PROPN":
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

    def file_save(self, pdf_name, url, chunk):
        '''
         Simplifed version of GUI save file & continue_func which saves
         created json files.

        Parameters
        ----------
        pdf_name : str
            name of pdf file to save as json
        url : str
            url of pdf file
        chunk : int
            current chunk of file being saved, corresponds to page number
        '''
        if self.name_prefix == None:
            self.name_prefix = pdf_name.split(".")[0].split("/")[2]
        output_filename = self.output_dir + "/" + \
            self.name_prefix + "_p" + str(chunk) + self.name_suffix

        if os.path.isfile(output_filename):
            if self.no_overwrite:
                print("Making file copy...")
                now = datetime.now()  # current date and time
                date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
                output_filename = self.output_dir + "/" + \
                    self.name_prefix + "_" + datatime + "_" + self.name_suffix
            else:
                print("File will be overwritten.")

        if len(self.cust_ents_dict) == 0:
            print("No annotations to save.")
        else:
            input_text = self.cust_ents_dict[chunk][0]
            entities = self.cust_ents_dict[chunk][1]
            input_text = re.sub(' +', ' ', input_text)
            ann_train_dict = mixed_type_2_dict(
                [(input_text, {'entities': entities})], chunk, pdf_name, url)
            dict_2_json(ann_train_dict, output_filename)
            print("Created %s." % output_filename)

        return output_filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepares data for medacy validation",
        epilog='python ValidationPreprocess.py model dir output_dir'
    )
    parser.add_argument(
        'model', help='path to trained model'
    )
    parser.add_argument(
        'dataset_dir', help='path to directory of dataset'
    )
    parser.add_argument(
        'output_dir', help='path of directory to save the converted  files trained on to'
    )

    parser.add_argument(
        '--val_output_dir', help='path of directory to save converted gold standard data to',
        action='store', default=None
    )

    parser.add_argument(
        '--file_prefix', help='file prefix to use to name new bratt and txt files of data',
        action='store', default=None
    )

    parser.add_argument(
        '--file_suffix', help='file suffix to find json files and name new ones',
        action='store', default='_td.json'
    )
    parser.add_argument(
        '--no_overwrite',
        help='Flag to prevent overwritting files.',
        action='store_true', default=False
    )

    args = parser.parse_args()
    model, dataset_dir, output_dir, val_output_dir, name_prefix, name_suffix, no_overwrite = args.model, args.dataset_dir, args.output_dir, args.val_output_dir, args.file_prefix, args.file_suffix, args.no_overwrite

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if val_output_dir is not None:
        if not os.path.exists(val_output_dir):
            os.makedirs(val_output_dir)
        dataset_to_bratt(dataset_dir, val_output_dir,
                         name_prefix=name_prefix, file_pattern="/*"+name_suffix)

    preprocess = ValidationPreprocess(
        model, dataset_dir, output_dir, name_prefix=name_prefix, name_suffix=name_suffix, no_overwrite=no_overwrite)
    preprocess.process_files()
