#!/bin/env python3

import spacy
from spacy.language import Language
from spacy.tokens import Span
from spacy.matcher import Matcher

from src.preparse import *

nlp = spacy.load('en_core_web_sm')

def adj_ent_entities(doc):
    # only deals with ADJ TRAT (or PLAN) = TRAT entities (e.g, 'low lodging' or 'rough awns')
    new_ents = []
    for ent in doc.ents:
        if ent.label_ in ('PLAN', 'TRAT') and ent.start != 0:
            prev_token = doc[ent.start - 1]
            # print('DEBUG: ', ent.text, ent.start, ent.label_, prev_token.text, prev_token.pos_, prev_token.dep_)
            if prev_token.pos_ == 'ADJ' and prev_token.dep_ == 'amod':
                new_ent = Span(doc, ent.start - 1, ent.end, label='TRAT')
                new_ents.append(new_ent)
            else:
                new_ents.append(ent)
        else:
            new_ents.append(ent)
    doc.ents = new_ents
    return doc

def trat_adj_entities(doc):
    # only deals with TRAT ADJ = TRAT entities (e.g., 'matures early')
    # CAVEAT: we still need to do deal with TRAT (be) ADJ (e.g., 'its protein levels are low')
    new_ents = []
    for ent in doc.ents:
        if ent.label_ in ('TRAT'):
            next_token = doc[ent.start + 1]
            # print('DEBUG: ', ent.text, ent.start, ent.label_, next_token.text, next_token.pos_, next_token.dep_)
            if next_token.pos_ == 'ADV' and next_token.dep_ == 'advmod':
                new_ent = Span(doc, ent.start, ent.end + 1, label='TRAT')
                new_ents.append(new_ent)    
            else:
                new_ents.append(ent)
        else:
            new_ents.append(ent)
    doc.ents = new_ents
    return doc

def plan_adj_entities(doc):
    #only deals with PLAN (be) ADJ = TRAT entities (e.g., 'awns are rough')
    new_ents = []
    for ent in doc.ents:
        if ent.label_ == "PLAN":
            # Because the entity is a spans, we need to use its root token. The head
            # is the syntactic governor of the person, e.g. the verb
            head = ent.root.head
            # print('DEBUG: entity head lemma', head.lemma_)
            if head.lemma_ == "be":
                # Check if the children contain an adjectival complement (acomp)
                acomps = [token for token in head.children if token.dep_ == "acomp"]
                # CAVEAT 1: For now let's assume adjectives are single-word
                # Later we should figure out the lowest and highest index among the adjectives
                acomp = acomps[0]
                # print('DEBUG: ', acomp, ent, "is a new TRAT (trait)")
                # CAVEAT 2: The document remains unchanged, so the term that will get stored
                # will be the original phrase 'awns are rough' instead of the standardized
                # 'rough awns'
                #
                # Having trouble defining a span from the first token of the Span 'ent' to the last token of 'acomp'
                # print('DEBUG: acomp', doc[acomp.i+1])
                new_ent = Span(doc, doc[ent.start].i, acomp.i+1, label="TRAT")
                new_ents.append(new_ent)
                # I would much rather overwrite the phrase as 'rough awns' like this DEBUG statement shows
                # by printing acomp + ent
            else:
                new_ents.append(ent)
        else:
            new_ents.append(ent)
    doc.ents = new_ents
    return doc

def get_matched_spans(doc, substring):

    matcher = Matcher(nlp.vocab)
    
    sdoc = nlp(substring)
    pattern = [{"ORTH": token.text} for token in sdoc] #allows matching multi-word pattern
    matcher.add(substring, None, pattern)
    
    result = []
    matches = matcher(doc)
    #print(matches)
    for match_id, start, end in matches:
#        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
#        print(match_id, string_id, start, end, span.text)
#        print(match_id, start, end, span.text)
        result.append(span)
    return result

def add_non_ovlp_ent(new_ent, master_ents):
    '''check if new entity (new_ent) overlaps with any in the master, and
       remove the old master entry if it is found to overlap.
       Return the original entity list with the new one added. '''

    if new_ent is None:
        return master_ents
    
    result = []
    for estab_ent in master_ents:
        if not ((new_ent.end_char >= estab_ent.start_char) and
            (new_ent.start_char <= estab_ent.start_char) or
            (estab_ent.end_char >= new_ent.start_char) and
            (estab_ent.start_char <= new_ent.start_char)):
            # no overlap detected, so add this established entity
            result.append(estab_ent)

    # add the new entity
    result.append(new_ent)
    return result

def add_ped_jrnl_entities(doc):
    '''add PED and JRNL entities derived from regex code'''

    # add in regex-derived PED & JRNL entries, being sure to remove other 
    # entities that overlap with them

    all_ents = list(doc.ents)
    regex_ents = preparse(doc.text)
    for ent_no in regex_ents[doc.text]:
        # The following ent_data is a dictionary for a new entity with keys like
        # {'start': 29, 'end': 33, 'label': 'PED', 'substring': 'A1/P2'}
        ent_data = regex_ents[doc.text][ent_no]

        # the following returns a list of spans in the original doc that
        # match ent_data['substring'], each indexed as
        # span_list[0].text, span_list[0].start, and span_list[0].end
        span_list = get_matched_spans(doc, ent_data['substring'])

        # Although there might be multiple matches, just work with the
        # first one for now
        new_ent = Span(doc, span_list[0].start, span_list[0].end, label=ent_data['label'])

        # Check to see if this new entity overlaps one called by the NLP.
        # If it does, remove the NLP-derived one.
        all_ents = add_non_ovlp_ent(new_ent, all_ents)

    doc.ents = all_ents
    return doc

@Language.component("compound_trait_entities")
def compound_trait_entities(doc):
    doc = adj_ent_entities(doc)
    doc = plan_adj_entities(doc)
    doc = trat_adj_entities(doc)
    doc = add_ped_jrnl_entities(doc)
    return doc

if __name__ == "__main__":

    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description = "parse agricultural text for key entities",
        epilog = 'Example: python3 agparse.py text (optional --model_dir dirname)'
    )
    parser.add_argument(
        'text', help = 'Any textual document to parse'
    )
    parser.add_argument(
        '--model_dir', help = 'Name of spacy NLP existing model'
    )

    if len(sys.argv)<0:
        parser.print_usage()
        sys.exit()
        
    args = parser.parse_args()
    text = args.text
    model_dir = args.model_dir
    
    if model_dir is not None:
        nlp = spacy.load(model_dir)

    nlp.add_pipe(compound_trait_entities, after='ner')
    doc = nlp(text)
    print("Text:")
    print(doc)
    print("\nEntities:")
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)

