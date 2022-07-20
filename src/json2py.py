#!/bin/env python3

import json
import sys
import os
import argparse

def dict_2_mixed_type(data):
    """ convert multi-document (list) or single-document (dict) JSON records
     to spaCy training ready objects.  E.g.:

     newest format = {'chunk': 1, 'doc': 'p.pdf', 'url': 'https://hello', 'date': 07_05_2022_13_57_08, crop: 'BARLEY', cvar: 'MAJA',
        'text': "All text here", 'entities': [[0, 3, 'TY1'], [4, 6, 'TY2']]}
     
     returns: [('All text here'), {'entities': [(0, 3, 'TY1'), (4, 6, 'TY2')]}]

     For some legacy json files saved by older versions of this program:

     simple = {'doc': 'p.pdf', 'url': 'https://hello', 'date': 07/05/2022, 'chunk': 1, 'sentences': {'sentence 1': {'entity 1': {'start': 0, 'end': 3, 'label': 'TY1'}, 'entity 2': {'start': 4, 'end': 6, 'label': 'TY2'}}}}

     returns: [('sentence 1', {'entities': [(0, 3, 'TY1'), (4, 6, 'TY2')]})]

     whereas

     complex = [{'doc': 'p.pdf', 'url': 'https://hello', 'date': 07/05/2022, 'chunk': 1, 'sentences': {'sentence 1': {'entity 1': {'start': 0, 'end': 3, 'label': 'TY1'}, 'entity 2': {'start': 4, 'end': 6, 'label': 'TY2'}}}}, {'doc': 'p.pdf', 'url': 'https://hello', 'chunk': 2, 'sentences': {'sentence 2': {'entity 1': {'start': 0, 'end': 4, 'label': 'TT1'}, 'entity 2': {'start': 6, 'end': 8, 'label': 'TY2'}}}}]

     returns: [('sentence 1', {'entities': [(0, 3, 'TY1'), (4, 6, 'TY2')]}),
               ('sentence 2', {'entities': [(0, 4, 'TT1'), (6, 8, 'TT2')]})]
    """

    # Newer format has 'text' field as opposed to sentence fields- a lack of this field indicates that we should
    # use older loading methods.
    try:
        data['text']
        return dict_2_mixed_type_2022(data)
    # Try older format if this fails
    except:
        if isinstance(data, dict):
            return dict_2_mixed_type_simple(data)
        else:
            result = []
            for record in data:
                subset = dict_2_mixed_type_simple(record)
                for sentence, entity_dict in subset:
                    result.append((sentence, entity_dict))
            return result

def dict_2_mixed_type_2022(data):
    """ Convert Nested JSON-like dictionary to the complex training
     data that spaCy requires. Specifically:
     {'doc': 'BarCvDescLJ11.pdf', 
      'url': 'https://smallgrains.ucdavis.edu/cereal_files/BarCvDescLJ11.pdf', 
      'date': '07_05_2022_13_57_08'
      'chunk': 2,
      'crop': 'BARLEY'
      'cvar': 'EIGHT-TWELVE'
      'text': "All document text"
      'entities': [[0, 3, 'TY1'], [4, 6, 'TY2'], ...]
      }
     is converted to:
       [('All document text', {'entities': [(0, 3, 'TY1'), (4, 6, 'TY2'), ...]})]
    """
    training_data = list()
    entity_list = dict()
    entity_list['entities'] = list()
    for entity in data['entities']:
        entity_list['entities'].append((entity[0], entity[1], entity[2]))
    training_data.append((data['text'], entity_list))
    return training_data

def dict_2_mixed_type_simple(data):
    """ Convert Nested JSON-like dictionary to the complex training
     data that spaCy requires. Specifically:
     {'doc': 'BarCvDescLJ11.pdf', 
      'url': 'https://smallgrains.ucdavis.edu/cereal_files/BarCvDescLJ11.pdf', 
      'date': '07/05/2022'
      'chunk': 2,
      'sentences': {'sentence 1': {'entity 1': 
                                       {'start': 0, 'end': 3, 'label': 'TY1'}, 
                                   'entity 2': 
                                       {'start': 4, 'end': 6, 'label': 'TY2'}
                                   }
                    }
      }
     is converted to:
       ('sentence 1', {'entities': [(0, 3, 'TY1'), (4, 6, 'TY2')]})
    """
    training_data = []
    
    for sentence in data['sentences']:
        entity_dict = dict()
        entity_list = []
        for entity_label in data['sentences'][sentence]:
            entity = data['sentences'][sentence][entity_label]
            try:
                tuple = (entity[0], entity[1], entity[2])
            except:
                tuple = (entity['start'], entity['end'], entity['label'])
            entity_list.append(tuple)
        entity_dict['entities'] = entity_list
        training_data.append((sentence, entity_dict))

    return(training_data)

def json_2_dict(fname):
    """ Convert a JSON object as a simple nested dict object"""

    data = dict()
    with open(fname) as fi:
        data = json.load(fi)

    return data

if __name__ == "__main__":

    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description = "convert JSON training data to python nested lists",
        epilog = "Example: python3 json2py.py jsonInput pyOutput"
    )
    parser.add_argument(
        'jsonInput', help = 'input json file.'
    )
    parser.add_argument(
        'pyOutput', help = 'output python file.'
    )

    if len(sys.argv)<2:
        parser.print_usage()
        sys.exit()
        
    args = parser.parse_args()
    infile, outfile = args.jsonInput,args.pyOutput

    data = json_2_dict(infile)

    fho = open(outfile, 'w')

    train_data = dict_2_mixed_type(data)
    fho.write('TRAIN_DATA = '+str(train_data)+"\n")
    fho.close()

