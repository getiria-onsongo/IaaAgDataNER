import random
import re
import spacy
from json2py import *
from pathlib import Path
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
    RAW_TRAIN_DATA = dict_2_mixed_type(training_data)
    
    # add entity labels
    labels = set()
    TRAIN_DATA = []
    for sent, annotations in RAW_TRAIN_DATA:
        ent_count = 0
        for ent in annotations.get("entities"):
            if ent[2] not in ('JRNL', 'PED'):
                ent_count += 1
                labels.add(ent[2])
        if ent_count != 0: # ignore 0-cnt lines where only anno was JRNL or PED
            TRAIN_DATA.append((sent, annotations))
                
    # print ('DEBUG: Labels include', labels)
    # [print('Adding label',label) for label in labels]
    [ner.add_label(label) for label in labels]

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
