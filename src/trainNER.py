#!/usr/bin/env python3

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
import PyPDF2
import re
from src.agData import *
from src.agParse import *
#from __future__ import unicode_literals, print_function


# NOTES:
# ***** FIX THE PARSER SO IT DOES NOT REMOVE SLASHES IN PEDIGREES
# - You need at a minimum 200 examples per entity to
# get a good model

# plac makes it easy to write command line tools

# PhraseMatcher lets you extract indices (locations) of string in a
# text. Aside, a good task might be taking a training data and seeing
# if we can extract equivalent matches

# goal is to extend the types of recognized labels to agriculturally-relevant ones such as
# CROP=crop
# CVAR=crop_variety
# PED=pedigree,
# ALAS=varietal_alias
# TRAT=trait
# JRNL=journal_reference
# PLAN=plant_anatomy
# PATH=pathogen,
# PPTD=plant_predisposition_to_disease



def wordOffset(lbl, doc, matchitem):
    '''
    :param lbl:
    :param doc:
    :param matchitem:
    :return: (start, end, label)

    This function converts the output of the PhraseMatcher to something
    usable in training. The training data needs a string index of
    characters (start, end, label) while the matched output uses index of
    words from an nlp document.
    '''
    o_one = len(str(doc[0:matchitem[1]]))
    subdoc = doc[matchitem[1]:matchitem[2]]
    o_two = o_one + len(str(subdoc)) + 1
    return (o_one, o_two, lbl)
def mergePEDtokens(doc):
    ''' By default spacy splits PED into different tokens. This
    function takes as input a spacy doc and merges PEDs into a
    single token. '''

    # If doc.text = 'a/b xx b/c', indexes will be [(0, 3), (7, 10)]
    # The deprecated doc.merge could merge token by a span of
    # the document text but this turns out to be prone to errors.
    #
    # The new implementation, retokenize, merges span of tokens as
    # opposed to span of texts. As a result, the current implementation
    # is a little bit more complicated. We need to convert the text
    # spans to token spans.

    # The line below finds all segments of the text that with the
    # form [space,alphanumeric/alphanumeric,space e.g., a/b
    indexes = [m.span() for m in re.finditer('[\w|\S]+/[\w|S]+', doc.text, flags=re.IGNORECASE)]

    # Spans should be sorted starting with the first one. We shouldn't need
    # this sort but just to be extra cautious we are sorting in ascending order.
    # NOTE: We are sorting to avoid O(N^2) running time if there are N spans
    # and N tokens. This implemention with spans sorted should be O(2N).
    indexes.sort()

    leftToken = -1 # Token containing beginning of PED
    rightToken = -1 # Token containing end of PED
    tokenSpans = [] # Will hold indexes equivalent except instead of spanning
    # doc.text it will span tokens
    span_index = 0
    (span_start, span_end) = indexes[span_index]

    # i: The index of the token within the parent document.
    # idx: The character offset of the token within the parent document.
    for token in doc:
        # Because by default Spacy uses spaces as one of the tokenizing
        # delimiter, and we are using space to demarcate the beginning of a
        # PED, token.idx will always correspond to beginning of a matching
        # doc.text span
        if token.idx == span_start:
            leftToken = token.i
        # Spans are right end exclusive. The right end token will be the
        # token just after the PED. In the merging, this token will be
        # excluded because spans are right end exclusive.
        elif token.idx == span_end + 1:
            rightToken = token.i
            # Add corresponding tokens span
            tokenSpans.append(doc[leftToken:rightToken])
            span_index = span_index + 1
            # If this was not the last span, get the new span to be converted
            if (span_index < len(indexes)):
                (span_start, span_end) = indexes[span_index]

    # If leftToken is greater than rightToken it means the last token contains a PED
    if leftToken > rightToken:
        tokenSpans.append(doc[leftToken:])

    # Once we have the matching doc.text spans converted to token spans, use the
    # new retokenizer
    with doc.retokenize() as retokenizer:
        for span in tokenSpans:
            retokenizer.merge(span)

    return doc

# Automate gathering training data

myFile = open("/Users/gonsongo/Desktop/research/iaa/Projects/python/IaaAgDataNER/Data/DavisLJ11/BarCvDescLJ11.pdf", mode="rb")

pdfReader = PyPDF2.PdfFileReader(myFile)

num_pages = pdfReader.numPages

# Get the first page
OnePage = pdfReader.getPage(35)


# Get text
OnePageText = OnePage.extractText()

# Close PDF file
myFile.close()


# print(OnePageText)


def trainModel(model=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Model loaded.. '%s'" % model)
    else:
        nlp = spacy.load('en_core_web_sm')
        print("Load  'en_core_web_sm' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add entity labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training, if present
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if model is None:
            nlp.begin_training()

        q1 = int(n_iter // 4)
        q2 = int(q1 * 2)
        q3 = int(q1 * 3)

        for itn in range(n_iter):
            if itn == q1:
                print("Training 25% done")
            elif itn == q2:
                print("Training 50% done")
            elif itn == q3:
                print("Training 75% done")
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
    print("Training complete!")
    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

def printEntities(doc):
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)

def offseter(lbl, doc, matchitem):
    '''
    :param lbl:
    :param doc:
    :param matchitem:
    :return: (start, end, label)

    This function converts the output of the PhraseMatcher to something
    usable in training. The training data needs a string index of
    characters (start, end, label) while the matched output uses index of
    words from an nlp document.
    '''
    o_one = len(str(doc[0:matchitem[1]]))
    subdoc = doc[matchitem[1]:matchitem[2]]
    o_two = o_one + len(str(subdoc))
    return (o_one, o_two, lbl)

if __name__ == "__main__":
    model = "agdata"
    output_dir="/Users/gonsongo/Desktop/research/iaa/Projects/python/IaaAgDataNER/agdata"
    n_iter = 100
    #trainModel(model,output_dir,n_iter)
    #trainModel(None, output_dir, n_iter)

    print("Loading trained model", output_dir)
    agdata_nlp = spacy.load(output_dir)
    print(agdata_nlp.pipe_names)

    print('\nTest 1..')
    test_text = ''' Merit 57 is a two-rowed spring malting barley. It was released by
    Busch Agricultural Resources in 2009. It was selected from the backcross Merit//Merit/2B94-5744
    made in 1996 in Fort Collins, Colorado.'''
    doc = agdata_nlp(test_text)
    for ent in doc.ents:
        print(ent.text + ' - ' + ent.label_)


    # If you want to retokenoze based on entities
    '''
    with doc.retokenize() as retokenize:
        for ent in doc.ents:
            retokenize.merge(ent)
    '''
