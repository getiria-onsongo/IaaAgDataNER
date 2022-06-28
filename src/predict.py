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


class Predict:
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
    self.spacy_only : bool
        flag to only uses spacy, not pos data to tag
    self.name_prefix : str
        start of file name for a new json file
    self.name_suffix : str
        end of file name for a new json file
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
    self.page_num : int
        current page number

    Methods
    -------
    process_files(self)
        process files by running through model then converting and saving
        json, bratt & txt of files
    extract_page_num(self, f : str, suffix : str)
        takes a file name and extracts its page number
    get_text(self, file : str)
        reads in a text file and returns as a string
    tag_ner_with_spacy(self, text: str) -> spacy.tokens.Doc:
        creates spacy doc from inputed text
    pre_tag(self, pdf_document : pyxpdf.Document, page_number : int)
        finds entities for a given page in a pdf
    get_pos(self, ent : str )
        finds the part of speech for an entity and expands if needed
    adj_combine_noun_ent(self, doc : spacy.Doc, current_index : int, ent :
    str, label : str)
        expands an entity to contain adjectives
    file_save(self, pdf_name : str, url : str, chunk : int)
        saves json for a file
    """

    def __init__(self, model_dir, dataset_dir, output_dir, spacy_only=False, name_prefix=None, name_suffix="_td.json", no_overwrite=False, spacy_model_name="en_core_web_lg", tags=["ALAS", "CROP", "CVAR", "JRNL", "PATH", "PED", "PLAN", "PPTD", "TRAT"]):
        self.model_dir = model_dir
        self.dataset_dir = dataset_dir
        self.output_dir = output_dir

        self.spacy_only = spacy_only
        self.name_prefix = name_prefix
        self.name_suffix = name_suffix
        self.no_overwrite = no_overwrite
        self.spacy_model_name = spacy_model_name  # spacy model to use for pos
        self.pos_model = spacy.load(self.spacy_model_name)
        self.nlp = spacy.load(self.model_dir)
        self.tags = tags

        self.cust_ents_dict = {}
        self.page_num = 0

        self.nlp.add_pipe("compound_trait_entities", after="ner")

    def process_files(self):
        """
        Gets the directory of pdfs, reads them in and then does ner tagging on them and
        saves as json.
        """
        files = glob.glob(self.dataset_dir+"/*_td.txt")
        print("%s files to process." % str(len(files)))

        for f in files:
            self.cust_ents_dict = {}
            text = self.get_text(f)
            page_number = self.extract_page_num(f, "_td.txt")
            self.pre_tag(text, page_number)
            json_name = self.file_save(f, "", page_number)

    def extract_page_num(self, f, suffix):
        """
        Gets page number for files where the page numbers are the one or two
        digits before the file suffix

        Parameters
        ----------
        f : str
            file name
        suffix : str
            file ending

        Returns page number as a string if found, otherwise an empty string
        """
        ints_as_strs = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        num = ""
        if f[len(f)-(len(suffix)+1)] in ints_as_strs:
            num = f[len(f)-(len(suffix)+1)]
            if f[len(f)-(len(suffix)+2)] in ints_as_strs:
                num = f[len(f)-(len(suffix)+2)] + num
        return num

    def get_text(self, file):
        """
        Gets text from a file

        Parameters
        ----------
        file : file name

        Returns text from file as a string.
        """
        text = ""
        with open(file) as f:
            text = f.read()
        return text

    def tag_ner_with_spacy(self, text: str) -> spacy.tokens.Doc:
        """
        Use NLP pipeline to identify named entities in the text.
        """
        doc = self.nlp(text)
        return doc


    def pre_tag(self, input_text, page_number):
        """
        Tags input text using model with ner tags

        Parameters
        ----------
        input_text : str
            text to tag
        page_number : str
            current page number
        """
        self.cust_ents_dict = {}
        doc = self.tag_ner_with_spacy(input_text)
        for ent in doc.ents:
            if ent.label_ in self.tags:
                if self.spacy_only is not True:
                    ent = self.get_pos(ent)
                if self.cust_ents_dict.get(page_number, False):
                    self.cust_ents_dict[page_number].append((ent.start_char, ent.end_char, ent.label_))
                else:
                    self.cust_ents_dict[page_number] = [(ent.start_char, ent.end_char, ent.label_)]
        if self.cust_ents_dict.get(page_number, False):
            tags = self.cust_ents_dict[page_number]
            self.cust_ents_dict[page_number] = [input_text, tags]


    def get_pos(self, ent):
        """
        Proceses a given entity with rules that use pos tag data to expand
        the entity span if needed.

        Parameters
        ----------
        ent : str
            entity to possibly expand span of

        Returns expanded entity.
        """
        doc = self.pos_model(ent.sent.text)
        if(len(doc[ent.start:ent.end]) > 0):
            current_index = doc[ent.start:ent.end][0].i
            label = ent.label_
            # functions that contain rules to expand the entity's span
            ent = self.adj_combine_noun_ent(doc, current_index, ent, label)
            # ent = self.num_combine_ent(doc, current_index, ent, label)
        return ent

    def adj_combine_noun_ent(self, doc, current_index, ent, label):
        """
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
        """
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

    def file_save(self, pdf_name, url, chunk):
        """
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
        """

        if self.name_prefix == None:
            path_no_suffix = pdf_name.split(".")[0].split("/")
            self.name_prefix = path_no_suffix[len(path_no_suffix)-1]
        output_filename = self.output_dir + "/" + \
            self.name_prefix + "_p" + str(chunk) + self.file_suffix
        if os.path.isfile(output_filename):
            if self.no_overwrite:
                print("Making file copy...")
                now = datetime.now()  # current date and time
                date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
                output_filename = self.output_dir + "/" + \
                    self.name_prefix + "_" + datatime + "_" + self.file_suffix
            else:
                print("File will be overwritten.")

        if len(self.cust_ents_dict) == 0:
            print("No annotations to save.")
        else:
            input_text = self.cust_ents_dict[chunk][0]
            entities = self.cust_ents_dict[chunk][1]
            ann_train_dict = mixed_type_2_dict(
                [(input_text, {"entities": entities})], chunk, pdf_name, url)
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
        'output_dir', help='path of directory to save the converted files trained on to'
    )
    parser.add_argument(
        '--spacy_only', help='only uses spacy model',
        action='store_true', default=False
    )
    parser.add_argument(
        '--convert_gold_standard', help='if goldstandard needs to be converted, path to that new folder',
        action='store', default=None
    )
    parser.add_argument(
        '--file_prefix', help='file prefix to use to name json files',
        action='store', default=None
    )
    parser.add_argument(
        '--file_suffix', help='file suffix to use to name new json files',
        action='store', default="_td.json"
    )
    parser.add_argument(
        '--no_overwrite',
        help='Flag to prevent overwritting files.',
        action='store_true', default=False
    )

    args = parser.parse_args()
    model, dataset_dir, output_dir, spacy_only, prefix, suffix, no_overwrite = args.model, args.dataset_dir, args.output_dir, args.spacy_only, args.file_prefix, args.file_suffix, args.no_overwrite

    if not os.path.exists(model):
        print("Path to model invalid")
    elif not os.path.exists(dataset_dir):
        print("Path to dataset invalid")
    else:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        preprocess = Predict(model, dataset_dir, output_dir, spacy_only=spacy_only,
                             name_prefix=prefix, name_suffix=suffix, no_overwrite=no_overwrite)
        preprocess.process_files()
