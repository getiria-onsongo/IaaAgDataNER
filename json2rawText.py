#!/bin/env python3

import json
import sys
import os
import argparse
import PyPDF2
import spacy
import glob

def json2raw(json_file_name, path_to_pdf, windowSize, fhandler):
    """ Takes as input a json document with training data (str), path to the PDF file that
     was used to generate the data (str), an integer (windowSize) defining the number of
     sentences flanking the training dataset when extracting a paragraph and file handler for the
     output file. NOTE: The output file should already be open.

     It writes to the output file  raw text in JSONL
     (newline-delimited JSON) file.

    NOTE: The recommendation by spacy is one input text per line and the total number of
    sentences flanking the training sentence should be roughly a paragraph length).

    Also NOTE: The input json file expected is the one generated using py2json.py.

    :param json_file_name: Name of json file with training data.
    :type json_file_name: str.
    :param json_file_name: Path to source PDF file
    :type json_file_name: str.
    :param windowSize: Number of sentences padding the training data sentence.
    :type windowSize: int.


    E.g.:

     {"doc": "BarCvDescLJ11.pdf",
     "url": "https://smallgrains.ucdavis.edu/cereal_files/BarCvDescLJ11.pdf",
     "chunk": "1",
     "sentences": {"Eight-Twelve is a six-rowed winter feed barley.":
        {
        "entity 1": {"start": 0, "end": 12, "label": "CVAR"}, "entity 2": {"start": 18, "end": 27, "label": "TRAT"},
        "entity 3": {"start": 28, "end": 34, "label": "TRAT"}, "entity 4": {"start": 35, "end": 39, "label": "CVAR"},
        "entity 5": {"start": 40, "end": 46, "label": "CROP"}
        }
    }
     returns: {"text": "EIGHT-TWELVE. Eight-Twelve is a six-rowed winter feed barley. It was released by the USDA-ARS and the Idaho AES in 1991."}

     where windowSize = 1

    text is a paragraph containing the sentence "Eight-Twelve is a six-rowed winter feed barley" which is used a training data
    with a 1 sentence before and after. To increase the paragraph, you can increase windowSize to a higher number.
    """

    f = open(json_file_name)
    data = json.load(f)
    f.close()

    nlp = spacy.load('en_core_web_lg')

    # Get sentences in training dataset
    trainingDataSentences = []

    for key in data['sentences'].keys():
        trainingDataSentences.append(key)

    # Open PDF file for reading
    pdfFile = open(path_to_pdf+"/"+data['doc'], mode="rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFile, strict=False)

    # Get pdf page where training data came from
    pageNumber = int(data['chunk'])
    pageIndex = pageNumber - 1
    page = pdfReader.getPage(pageIndex)
    pageText = page.extractText()

    # Extract sentences from pdf page and put them in a list
    pageText = pageText.replace('\n', '')
    doc = nlp(pageText)

    pageSentences = []
    for sent in doc.sents:
        pageSentences.append(sent.text)

    cnt = 0
    for trainSent in trainingDataSentences:
        paragraph = ""
        try:
            sent_num = pageSentences.index(trainSent)
            start = sent_num - windowSize
            end = sent_num + windowSize + 1  # slicing grabs up to but not the end
            if (start < 0):
                start = 0
            # No need to check if end > length of list. If it is, slice will
            # grab everything up to the end
            sent_list = pageSentences[start:end]
            beforeChars=0
            for i in range(len(sent_list)):
                paragraph = paragraph + sent_list[i]
                print("i=",i)
                print("sent_num=", sent_num)
                if i < windowSize:
                    beforeChars = beforeChars + len(sent_list[i])
            # Remove double quotes otherwise they will mess up the jsonl format. A double quote
            # will be considered end of text
            paragraph = paragraph.replace('"', '')
            fhandler.write("{\"text\":\"" + paragraph + "\"}")
            fhandler.write("\n")
            cnt = cnt + 1

            print("\n----")
            print("beforeChars=",beforeChars)
            print(paragraph)
            print("len(paragraph=",len(paragraph))
            print(data['sentences'][trainSent])
            for ent, vals in data['sentences'][trainSent].items():
                print(ent,vals)
                print(vals['start']+beforeChars)
                print(vals['end']+beforeChars)
                print(paragraph[vals['start']+beforeChars:vals['end']+beforeChars],vals['label'])
            print("----\n")

        except ValueError:
            # If sentence is not present, a ValueError will be
            # raised. Just ignore it for now.
            continue

    print("Matched " + str(cnt) + " out of " + str(len(trainingDataSentences)) + " sentences in file: " + json_file_name)
def convert_files(windowSize, fprefix, fsuffix, input_dir, output_dir, output_prefix):
    """ Add docstring """
    " Name of the output file is the prefix out the input file with .jsonl added at the end."

    fhandler = open(output_dir + "/" + output_prefix+".jsonl", "w")
    for fname in glob.glob(input_dir+"/"+fprefix+'*'+fsuffix):
        json2raw(fname, input_dir, windowSize, fhandler)
    fhandler.close()

if __name__ == "__main__":
    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description="Create raw text for pre-training in jsonl format",
        epilog='Example: python3 json2rawText.py 3 barley_p _td.json Data/DavisLJ11  Data/DavisLJ11/rawText DavisLJ11_raw_text'
    )

    parser.add_argument(
        'windowSize', help='integer for number of sentences padding the training data sentence'
    )

    parser.add_argument(
        'fprefix', help='File prefix for training data in json format.'
    )
    parser.add_argument(
        'fsuffix', help='File suffix for training data in json format.'
    )
    parser.add_argument(
        'input_dir', help='input directory where the training data can be found.'
    )
    parser.add_argument(
        'output_dir',
        help='Output directory (must exist already) to place output file in jsonl format.'
    )

    parser.add_argument(
        'output_prefix',
        help='Output filename base prefix for combined raw text from all json files.'
    )


    if len(sys.argv) < 6:
        parser.print_usage()
        sys.exit()

    args = parser.parse_args()
    windowSize, fprefix, fsuffix, input_dir, output_dir, output_prefix = int(
        args.windowSize), args.fprefix, args.fsuffix, args.input_dir, args.output_dir, args.output_prefix

    convert_files(windowSize, fprefix, fsuffix, input_dir, output_dir, output_prefix)