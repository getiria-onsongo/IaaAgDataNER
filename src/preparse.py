#!/bin/env python3

import json
import sys
import re
import argparse

def find_ped(text):
    """ Find pedigrees in Purdy notation among text blocks.
        Returns a list of all pedigree substrings found. """

    # Verified to match all of the following when followed by the words
    #   cross, pedigree, hybrid:
    #
    # Steveland/Luther//Wintermalt
    # I1162-19/J-126//WA1245///Steptoe
    # Sma1/Sunbar 401/3/Gus/Kombyne//Sma1
    # WA Sel 3564/Unitan//UT Short2*2
    # Ataco/Achira//Higo x UC 960
    # Steptoe/2*Diamant /3/Minn Dwarf 64.98-8/Briggs/4/Asse
    # Foma/Triple Bearded Mariout//White Winter (WA6194- 63)/3/Blazer
    # UT-S.D. B1-1009/M72-395/3/Utah Short #2//ID633019/Woodvale/4/Steptoe/M27//Westbred Gustoe
    # Atlas *3/CIho 3920-1//Atlas 46/3/4* Atlas/CIho 1179//2* Atlas 57
    # TR440/Clark = Klages//Zephyr/Centennial/3/Clark
    # Woodvale//Primus/SD67-297/3/Steptoe/4/UT Short #1
    # A308 (Lewis somaclonal line)/Baronesse
    # Betzes*7/"Strip Tease"
    # California Mariout *4/Arivat
    # Harrington/Orca//D172 (Shyri/Galena)
    # CM 67/3*Briggs/4/Briggs*4/3/California Mariout*4/CIho 1179//2*California Mariout*6/Club Mariout
    # Diamant/St. 1402964-9
    # 60Ab1810-53/Hector = Betzes/Domen//Hector
    # X1275/Sunbar 458//Gloria 'S'/Copal 'S'
    #
    # Fails on this one (Not Purdy notation):
    #   Aramir*((Cebaco 6721*(Julia/3/Volla*L100)) -- problematic

    breed = r'\d*\*?\s*(?:(?:[\w\.\'\"\-\(\)\#]+)\s*){1,5}\*?\d*'
    cross = r'/\d+/|/+'
    prelude = r'(?:cross|hybrid|pedigree|=)\s+'
    ped = prelude + "(" + breed + "(?:(?:" + cross + ")" + breed + ")*)"
    ped_re = re.compile(ped)
    result = ped_re.findall(text)
    # get rid of trailing sentence fragments (distinguished from periods that
    #    are part of the name of a variety
    result = [re.sub(r'\.\s[^/]*$', '', item) for item in result]
    # trim off trailing periods and whitespace (e.g., at the end of a sentence)
    result = [re.sub(r'[\.\s]+$', '', item) for item in result]
    return result

def find_jrnl(text):
    """ Find journal citations among text blocks.
        Returns a list of all journal citation substrings found. """

    # Verified to match all of the following:
    #
    # Crop Science 25:1123 (1985)
    # Crop Science 9(4):521 (1969)
    # Crop Science 41:265-266 (2001)
    # Crop Science 30(2): 421 (1990)
    # Journal of American Society of Agronomy 33:252 (1941)

    citation = r'(?:[A-Z][\w\.]+)(?:\s+[\w\.]+){0,5}\s+\d+(?:\(\d+\))?\s*:\s*\d+(?:-\d+)?\s+\(\d+\)'
    cit_re = re.compile(citation)
    return cit_re.findall(text)

def preparse(text):
    """ Parse out positions and identities of all pedigree and journal citation
        strings in a text block. 
        o return dictionary of matches with their information
        TODO: also consider outputting to STDERR the input text with matched 
        entities replaced by simple IDs (PED1, PED2, JRNL1, JRNL2, ...) """

    result = dict()
    result[text] = dict()

    # group together all text matches, sequentially by type
    ped_matches = find_ped(text)
    jrnl_matches = find_jrnl(text)
    matches = ped_matches + jrnl_matches
    match_types = ['PED'] * len(ped_matches) + ['JRNL'] * len(jrnl_matches)
    
    for i in range(0, len(matches)):
        entity_id = 'entity '+str(i+1)
        start_pos = text.find(matches[i])
        end_pos = start_pos+len(matches[i])-1
        result[text][entity_id] = {'start': start_pos, 'end': end_pos, 'label': match_types[i], 'substring': matches[i]}

    return result

    
if __name__ == "__main__":

    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description = "Parse out items poorly handled by NLP (e.g., pedigrees, journal citations)",
        epilog = 'Example: python3 preparse.py text (optional --outfile myOut.json)'
    )
    parser.add_argument(
        'text', help = 'Any textual document to pre-parse'
    )
    parser.add_argument(
        '--outfile', help = 'Name of output file for JSON formatted results'
    )

    if len(sys.argv)<0:
        parser.print_usage()
        sys.exit()
        
    args = parser.parse_args()
    text = args.text
    outfile = args.outfile
    
    if outfile is None:
        print(preparse(text))
    else:
        with open(outfile, "w") as fho:
            json.dump(preparse(text), fho)

