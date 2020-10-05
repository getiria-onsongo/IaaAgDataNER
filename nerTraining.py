import random
import re
import spacy
from json2py import *
from pathlib import Path
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER,CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import minibatch, compounding
from spacy.util import compile_infix_regex

def trainModel(model=None, training_file=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""

    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Model loaded.. '%s'" % model)
    else:

        if training_file is None:
            print("A JSON training file must be provided. Exiting.\n")
            return
    
# DO NOT create a blank model like below! We absolutely need POS information, and that 
#  won't be included with a blank model!!
#        nlp = spacy.blank("en")  # create blank Language class
#        print("Created blank 'en' model")
        
        nlp=spacy.load('en_core_web_sm') # create English model as basic class to augment
        print("Created pre-trained 'en' model")
        

        # The code below is custom to agData. It modifies how the
        # parser works to avoid splitting pedigrees

        # Tell spacy not to split between hyphens
        infixes = (
                LIST_ELLIPSES
                + LIST_ICONS
                + [
                    r"(?<=[0-9])[+\-\*^](?=[0-9-])",
                    r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                        al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
                    ),
                    r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
                    r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
                ]
        )
        infix_re = compile_infix_regex(infixes)
        nlp.tokenizer.infix_finditer = infix_re.finditer

        # Tell spaCy not to split on slashes (/). This will preserve PEDs.
        # There is a chance we will get unintended side effects but we have
        # not encountered one yet. We should rigorously test this at a later stage
        digit_hyphen_re = re.compile(r'[\w|\S]+/[\w|\S]+')
        nlp.tokenizer.token_match = digit_hyphen_re.search

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # load training data from a file
    training_data = json_2_dict(training_file)
    TRAIN_DATA = dict_2_mixed_type(training_data)
    
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
            # print("Losses", losses)

    print("Training complete!")

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

if __name__ == "__main__":
    pass
