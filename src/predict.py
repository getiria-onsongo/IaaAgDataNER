import os.path
import re
import glob
from agParse import *
from json2py import *
from py2json import *
from datetime import datetime
from pyxpdf import Document
from pyxpdf.xpdf import TextControl
from json2bratt import conversion
from dataset2bratt import extract_page_num

class Predict:
    """
    A class to do predictions on data using the trained model

    ...
    Attributes
    ----------
    self.model_dir : str
        path to trained model for ner tagging
    self.dataset_dir : str
        path to dataset to predict on
    self.output_dir : str
        path to output predictions to
    self.spacy_only : bool
        flag to only uses spacy model and not the part-of-speech based entity
        expansion feature
    self.name_json : str
        start of file name for a new json file.
        Ex: for creating predictions with files in the naming scheme
        barley_p1_td.json ... barley_p37_td.json, the prefix would be barley_p
        as it is the start of all file names
    self.json_suffix : str
        end of file name for a new json file
        Ex: for creating predictions with files in the naming scheme
        barley_p1_td.json ... barley_p37_td.json, the suffix would be _td.json
        as it is the end of all file names
    self.dataset_suffix
        endings of files from dataset directory to read in and predict on,
        for files like barley_p1_td.txt or barley_p12_td.txt, the dataset suffix
        would be _td.txt as it is the part of the file name all the files share
    self.no_overwrite: bool
        flag for creating new files instead of overwritting, which is the
        default. with this flag, files will have the exact time of generation
        between the file prefix and suffix instead of the page number to make
        sure the file name is unique
    self.spacy_model_name : str
        name of spacy model to use for part of speech, the default is
        "en_core_web_lg"
    self.pos_model : spacy.Language
        model for part of speech tagging
    self.nlp : spacy.Language
        model for ner tagging
    self.tags : list[str]
        list of possible ner tags
    self.cust_ents_dict : dict
        dictionary to keep track of entities found

    Methods
    -------
    process_files(self)
        process files by running through model then converting and saving
        as json files
    get_text(self, file : str)
        reads in file and returns contents as a string
    tag_ner_with_spacy(self, text: str) -> spacy.tokens.Doc:
        creates spacy doc from inputed text and the trained ner spacy model
    pre_tag(self, pdf_document : pyxpdf.Document, page_number : int)
        finds entities for a given page in a pdf
    get_pos(self, ent : str )
        finds the part of speech for an entity and expands if needed
    adj_combine_noun_ent(self, doc : spacy.Doc, current_index : int, ent :
    str, label : str)
        expands an entity to contain adjectives
    file_save(self, pdf_name : str, url : str, chunk : int)
        saves json for a given page
    """

    def __init__(self, model_dir, output_dir, dataset_dir=None, spacy_only=False, json_prefix=None, json_suffix="_td.json", dataset_suffix="_td.txt", no_overwrite=False, spacy_model_name="en_core_web_lg"):
        self.model_dir = model_dir
        self.dataset_dir = dataset_dir
        self.output_dir = output_dir

        self.spacy_only = spacy_only
        self.json_prefix = json_prefix
        self.dataset_suffix = dataset_suffix
        self.json_suffix = json_suffix
        self.no_overwrite = no_overwrite
        self.spacy_model_name = spacy_model_name

        self.pos_model = spacy.load(self.spacy_model_name)
        self.nlp = spacy.load(self.model_dir)
        self.tags = ["ALAS", "CROP", "CVAR", "JRNL", "PATH", "PED", "PLAN", "PPTD", "TRAT"]
        self.cust_ents_dict = {}
        self.nlp.add_pipe("compound_trait_entities", after="ner")


    def process_files(self, files=None, json=False):
        """
        Gets a list of txt files from the dataset directory, then does ner
        tagging on them before saving as json.
        """
        if files == None:
            files = glob.glob(self.dataset_dir+"/*"+self.dataset_suffix)
        print("%s files to process." % str(len(files)))

        for f in files:
            self.cust_ents_dict = {}
            if json:
                text = self.get_json_text(f)
            else:
                text = self.get_text(f)
            page_number = extract_page_num(f, self.dataset_suffix)
            self.pre_tag(text, page_number)
            json_name = self.file_save(f, "", page_number)

    def get_text(self, file : str):
        """
        Loads text from a given  file to be able to predict on it

        Parameters
        ----------
        file : file name

        Returns text from file as a string.
        """
        text = ""
        with open(file) as f:
            text = f.read()
        return text

    def get_json_text(self, file : str):
        """
        Loads text from a given json file to be able to predict on it

        Parameters
        ----------
        file : file name

        Returns text from json files as a string.
        """
        json_dict = json_2_dict(file)

        return next(iter(json_dict["sentences"]))

    def tag_ner_with_spacy(self, text: str) -> spacy.tokens.Doc:
        """
        Use NLP pipeline to identify named entities in the text.
        """
        doc = self.nlp(text)
        return doc

    def pre_tag(self, input_text : str, page_number : int):
        """
        Tags input text using model for ner taging and saves to
        the cust_ent_dict dictionary

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
        Proceses a given entity with rules that use part of speech data to
        expand the entity span if needed.

        Parameters
        ----------
        ent : str
            entity to possibly expand span of

        Returns expanded entity
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

    def file_save(self, pdf_name : str, url : str, chunk : str):
        """
        Simplifed version of GUI save file & continue_func which saves
        created json files to the output directory

        When the json file name is generated the format is
        "prefix page-number suffix", so for saving a file named barley_p1_td.json,
        the prefix would be "barley_p",the page number 1, and the suffix _td.json.

        Prefix extraction works with file names in the format
        "text_ page-number suffix", the prefix will be any text before the
        first underscore and then "_p" added on to the end

        Parameters
        ----------
        pdf_name : str
            name of pdf file to save as json
        url : str
            url of pdf file
        chunk : int
            current chunk of file being saved, corresponds to page number
        """
        name = self.json_prefix
        if name == None:
            path_no_suffix = pdf_name.split(self.dataset_suffix)[0].split("/")
            name = path_no_suffix[len(path_no_suffix)-1].split("_p")[0] + "_p"
        output_filename = self.output_dir + "/" + name + chunk + self.json_suffix

        if os.path.isfile(output_filename):
            if self.no_overwrite:
                print("Making file copy...")
                now = datetime.now()  # current date and time
                date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
                output_filename = self.output_dir + "/" + name + date_time + "_p" + chunk + self.json_suffix
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
        epilog='python predict.py model dir output_dir'
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
        '--json_prefix', help='prefix to use to name json files',
        action='store', default=None
    )
    parser.add_argument(
        '--json_suffix', help='suffix to use to name new json files',
        action='store', default="_td.json"
    )
    parser.add_argument(
        '--dataset_suffix', help='suffix to use to find files in dataset directory to predict on',
        action='store', default="_td.txt"
    )
    parser.add_argument(
        '--no_overwrite',
        help='Flag to prevent overwritting files.',
        action='store_true', default=False
    )

    args = parser.parse_args()
    model, dataset_dir, output_dir, spacy_only, json_prefix, json_suffix, dataset_suffix, no_overwrite = args.model, args.dataset_dir, args.output_dir, args.spacy_only, args.json_prefix, args.json_suffix, args.dataset_suffix, args.no_overwrite

    if not os.path.exists(model):
        print("Path to model invalid")
    elif not os.path.exists(dataset_dir):
        print("Path to dataset invalid")
    else:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        preprocess = Predict(model, dataset_dir, output_dir, spacy_only=spacy_only,
                             json_prefix=json_prefix, json_suffix=json_suffix, dataset_suffix=dataset_suffix, no_overwrite=no_overwrite)
        preprocess.process_files()
