#!/bin/env python3

import spacy
import re
import sys
import argparse

#
# TODO:
#
# Convert agData.py into JSON so that we can avoid the dangerous code
# I've written (allowing someone to import a python file they choose for
# execution).
#
# Break up training data into 37 parts (for each page) and then
# creating code to leave out one page and test it with a model generated
# from the other 36.

#
# Global Variables:
#
# entity_tally - Global dict with count of observations for all entity types
#                (e.g., 'TRAT', 'CROP', 'CVAR') in each of the following
#                categories ('match', 'overlap', 'mislabel', 'false_pos',
#                            'false_neg')
# e.g.,
#    >>> entity_tally['TRAT']
#    {'match': 210, 'overlap': 8, 'mislabel': 3, 'false_pos': 7, 'false_neg': 7}

entity_tally = dict()

def apply_model_2_text(nlp_model, text):
    """apply a compiled spacy NLP model to the text string provided"""

    entities = []
    doc = nlp_model(text)
    for ent in doc.ents:
        tup = (ent.start_char, ent.end_char, ent.label_)
        # print(ent.text, ": ", tup)
        entities.append(tup)

    return entities

def tally_calls(truth, model):
    """compare model results to ground truth and tally in global dict"""
    # Both truth and model data inputs are lists of tuples like this:
    # [(0, 12, 'CVAR'), (18, 27, 'TRAT'), (28, 34, 'TRAT'), (35, 39, 'CVAR')]

    marked_to_remove = [] # list of tuples to remove once they are dealt with
    
    for model_tuple in model:
        ent_label = model_tuple[2]
        for truth_tuple in truth:
            # find all exact matches, tally them 
            if same_tuple(model_tuple, truth_tuple):
                tally_label_state(ent_label, 'match')
                marked_to_remove.append(model_tuple)
            # find all exact phrases with wrong label, tally them 
            elif same_coords(model_tuple, truth_tuple):
                tally_label_state(ent_label, 'mislabel')
                marked_to_remove.append(truth_tuple)
                marked_to_remove.append(model_tuple)
            # find all labels that overlap non-exactly, tally them 
            elif coords_overlap(model_tuple, truth_tuple):
                tally_label_state(ent_label, 'overlap')
                marked_to_remove.append(truth_tuple)
                marked_to_remove.append(model_tuple)

    # need to remove all the tuples that we've dealt with in both lists
    model = remove_tuples(model, marked_to_remove)
    truth = remove_tuples(truth, marked_to_remove)

    # Any entries left in the model list are all false positives
    try:
        for ent_tuple in model:
            ent_label = ent_tuple[2]
            tally_label_state(ent_label, 'false_pos')
    except TypeError:
        True

    # Any entries left in the truth list are all false negatives
    try:
        for ent_tuple in truth:
            ent_label = ent_tuple[2]
            tally_label_state(ent_label, 'false_neg')
    except TypeError:
        True

def tally_label_state(label, state):
    """record an instance of state 'state' for the label 'label' 
       labels might include ('TRAT', 'CROP', 'CVAR',...)"
       states include ('match', 'overlap', 'mislabel', 'false_pos', 'false_neg')
    """
#    print("Tallying: ", label, state)
    try:
        # If no error, a 'state' with 'label' was already seen
        entity_tally[label][state] += 1
#        print(1, label, state, entity_tally[label][state])
    except KeyError:
        try:
            # If no error, we've seen other 'states' for 'label', but not
            # this one
            entity_tally[label][state] = 1
#            print(2, label, state, entity_tally[label][state])
        except KeyError:
            # we've never tallied anything yet for this 'label'
            entity_tally[label] = dict()
            entity_tally[label][state] = 1
#            print(3, label, state, entity_tally[label][state])

def same_tuple(tuple1, tuple2):
    """Checks whether two tuples have the same coordinates and label"""
    if tuple1[0] == tuple2[0] and tuple1[1] == tuple2[1] and tuple1[2] == tuple2[2]:
        return True
    else:
        return False

def same_coords(tuple1, tuple2):
    """Checks whether two tuples have the same coordinates, irrespective
       of the label that is attached.
       e.g., tuple1 = (0, 17, 'CVAR'), tuple2 = (0, 17, 'CROP')
       still returns True, even though 'CVAR' and 'CROP' differ.
    """
    if tuple1[0] == tuple2[0] and tuple1[1] == tuple2[1]:
        return True
    else:
        return False

def coords_overlap(tuple1, tuple2):
    """Checks whether two tuples have overlapping coordinates
       e.g., tuple1 = (18, 35, 'CVAR'), tuple2 = (22, 41, 'CROP')
       returns True irrespective of whether their labels match
    """
    if ((tuple1[1] >= tuple2[0]) and (tuple1[0] <= tuple2[0]) or
         (tuple2[1] >= tuple1[0]) and (tuple2[0] <= tuple1[0])):
        return True
    else:
        return False

def remove_tuples(master_list, removal_list):
    """Walk through a master_list and remove all items in the removal_list"""

    for bygone in removal_list:
        for tuple in master_list:
            if tuple == bygone:
                master_list.remove(tuple)

def print_stats():
    """Print tallies for all named entities"""

    print("Entity\tStatus\tCount")
    
    for label in entity_tally:
        sum = 0
        for state in entity_tally[label]:
            count = entity_tally[label][state]
            print(label+"\t"+state+"\t"+str(count))
            sum += count
        print(label+"\tTOTAL\t"+str(sum))
    
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

    for truth_record in truth.TRAIN_DATA:
#        print(truth_record)
        model_results = apply_model_2_text(nlp, truth_record[0])
#        print("compared with: ", model_results)
        tally_calls(truth_record[1]['entities'], model_results)

    print_stats()

