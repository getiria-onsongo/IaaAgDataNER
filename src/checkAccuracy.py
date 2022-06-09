#!/bin/env python3

import spacy
import re
import sys
from json2py import *
import argparse

#
# Global Variables:
#
# entity_tally - Global dict with count of observations for all entity types
#                (e.g., 'TRAT', 'CROP', 'CVAR') in each of the following
#                categories ('match', 'overlap', 'mislabel', 'false_pos',
#                            'false_neg', 'total')
# e.g.,
#    >>> entity_tally['TRAT']
#    {'match': 210, 'overlap': 8, 'mislabel': 3, 'false_pos': 7, 'false_neg': 7,
#     'total': 235}

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

def clear_tally():
    """ clear out the tally stats """
    global entity_tally
    entity_tally = dict()

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

    # print("model leftovers: "+str(model))
    # print("truth leftovers: "+str(truth))

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
       Note that a special state 'total' is incremented with any tally.
    """
    global entity_tally
    # print("Tallying: ", label, state)
    try:
        # If no error, a 'state' with 'label' was already seen
        entity_tally[label][state] += 1
        # print(1, label, state, entity_tally[label][state])
    except KeyError:
        try:
            # If no error, we've seen other 'states' for 'label', but not
            # this one
            entity_tally[label][state] = 1
            # print(2, label, state, entity_tally[label][state])
        except KeyError:
            # we've never tallied anything yet for this 'label'
            entity_tally[label] = dict()
            entity_tally[label][state] = 1
            # print(3, label, state, entity_tally[label][state])

    # now accumulate the total counts
    try:
        entity_tally[label]['total'] += 1
    except KeyError:
        entity_tally[label]['total'] = 1

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
            if same_tuple(tuple, bygone):
                master_list.remove(tuple)
    return master_list

def print_stats(outfile=None):
    """Print tallies for all named entities"""

    if outfile is None:
        print("Entity\tStatus\tCount\tPercent")
    else:
        fo = open(outfile, "w")
        fo.write("Entity\tStatus\tCount\tPercent\n")
        
    
    for label in entity_tally:
        for state in entity_tally[label]:
            if state != 'total':
                count = entity_tally[label][state]
                total = entity_tally[label]['total']
                pcnt = round(100*count/total, 1)
                if outfile is None: # print to STDOUT
                    print(label+"\t"+state+"\t"+str(count)+"\t"+str(pcnt))
                else:
                    fo.write(label+"\t"+state+"\t"+str(count)+"\t"+str(pcnt)+"\n")

def check_model_accuracy(training_file, model_dir, outfile=None):
    """apply NLP model to docs in training_file and assess accuracy"""

    training_data = json_2_dict(training_file)
    TRAIN_DATA = dict_2_mixed_type(training_data)

    #
    # Open the training file, grab each line and apply the model
    # to each line of text in the training file.
    #
    nlp = spacy.load(model_dir)

    for truth_record in TRAIN_DATA:
        # print(truth_record)
        model_results = apply_model_2_text(nlp, truth_record[0])
        # print("compared with: ", model_results)
        tally_calls(truth_record[1]['entities'], model_results)

    print_stats(outfile)
    
    
if __name__ == "__main__":

    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description = "Compare predicted NER components with trained data",
        epilog = 'Example: python3 checkAccuracy.py modelDir testFile (optional --outfile fname)'
    )
    parser.add_argument(
        'model_dir', help = 'model directory. This is the NLP model built by spaCy.'
    )
    parser.add_argument(
        'truth_file', help = 'Ground truth training data that we are comparing to.'
    )
    parser.add_argument(
        '--outfile', default = None, help = 'Output file for accuracy statistics\
        Default = STDOUT'
    )

    if len(sys.argv)<2:
        parser.print_usage()
        sys.exit()
        
    args = parser.parse_args()
    model_dir, training_file, outfile = args.model_dir, args.truth_file, args.outfile
    training_file = training_file.replace(".py", "")

    check_model_accuracy(training_file, model_dir, outfile)
