#!/bin/env python3

import json
import sys
import os
import argparse

#
# WARNING: the python file with the data (e.g., agData.py) must be in the
#  same directory as the running script. Otherwise the import of agData.py
#  doesn't work (you get at ModuleNotFoundError).
#
# Since we are only using this to convert everything to JSON once and for
# all, I won't bother figuring out how to get the PYTHONPATH properly changed
# or whatever needs to happen to fix this.

def mixed_type_2_dict(data, chunk, doc='', url=''):
    """ Convert ('sentence 1', {'entities': [(0, 3, 'TY1'), (4, 6, 'TY2')]})
     to:
     {'doc': 'BarCvDescLJ11.pdf', 
      'url': 'https://smallgrains.ucdavis.edu/cereal_files/BarCvDescLJ11.pdf', 
      'chunk': 2, 
      'sentences': {'sentence 1': {'entity 1': 
                                       {'start': 0, 'end': 3, 'label': 'TY1'}, 
                                   'entity 2': 
                                       {'start': 4, 'end': 6, 'label': 'TY2'}
                                   }
                    }
      }
    """

    result = dict()
    result['doc'] = doc
    result['url'] = url
    result['chunk'] = chunk
    result['sentences'] = dict()

    for record in data:
        sentence = record[0]
        entities = record[1]['entities']
        result['sentences'][sentence] = dict()
        for i in range(0,len(entities)):
            entity_id = 'entity '+str(i+1)
#            result['sentences'][sentence][entity_id] = dict()
            result['sentences'][sentence][entity_id] = {'start': entities[i][0], 'end': entities[i][1], 'label': entities[i][2]}

    return result

def dict_2_json(mydict, fname):
    """ Convert a structured nested dict object to a JSON dump"""

    with open(fname, "w") as fho:
        json.dump(mydict, fho)

if __name__ == "__main__":

    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description = "convert python nested lists to JSON",
        epilog = "Example: python3 py2json.py pyInput jsonOutput (optional --doc 'BarCvDescLJ11.pdf' ; --url 'http://smalgrains.ucdavis.edu' ; --chunk 2"
    )
    parser.add_argument(
        'pyInput', help = 'input python file.'
    )
    parser.add_argument(
        'jsonOutput', help = 'output json file.'
    )
    parser.add_argument(
        '--doc', help = 'name of the source document for the information'
    )
    parser.add_argument(
        '--url', help = 'source URL for the information'
    )
    parser.add_argument(
        '--chunk', help = 'integer page or chunk number within the document'
    )

    if len(sys.argv)<2:
        parser.print_usage()
        sys.exit()
        
    args = parser.parse_args()
    input_file, outfile = args.pyInput,args.jsonOutput
    infile = input_file.replace(".py", "")

    data = __import__(infile)
    TRAIN_DATA = data.TRAIN_DATA

    train_dict = mixed_type_2_dict(TRAIN_DATA, args.chunk, args.doc, args.url)
    dict_2_json(train_dict, outfile)
