#!/bin/env python3

import spacy
import re
import sys
import argparse

#
# TODO:
#
# 1. fix apply_model_2_text so it records counts of matches,
# overlapping-mismatches, false-pos and false-neg for each type of entity
# in a master dictionary
#
# 2. convert agData.py into JSON so that we can avoid the dangerous code
# I've written (allowing someone to import a python file they choose for
# execution).
#
# 3. break up training data into 37 parts (for each page) and then
# creating code to leave out one page and test it with a model generated
# from the other 36.

def apply_model_2_text(nlp_model, text):
    """apply a compiled spacy NLP model to the text string provided"""

    doc = nlp_model(text)
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)

if __name__ == "__main__":

    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description = "Compare predicted NER components with trained data",
        epilog = 'Example: python3 checkAccuracy.py modelDir trainingFile'
    )
    parser.add_argument(
        'model_dir', help = 'model directory. This is the NLP model built by spaCy.'
    )
    parser.add_argument(
        'truth_file', help = 'Ground truth training data that we are comparing to.'
    )

    if len(sys.argv)<2:
        parser.print_usage()
        sys.exit()
        
    args = parser.parse_args()
    model_dir, training_file = args.model_dir, args.truth_file
    training_file = training_file.replace(".py", "")

    #
    # Open the training file, grab each line and apply the model
    # to each line of text in the training file.
    #
    nlp = spacy.load(model_dir)

    # The following loads data into an array TRAIN_DATA
    # It is assumed that training data is of the expected form, and not
    # some malicious code. This code should not be used by untrusted parties
    truth = __import__(training_file)

    for record in truth.TRAIN_DATA[0:5]:
        print(record)
        apply_model_2_text(nlp, record[0])

