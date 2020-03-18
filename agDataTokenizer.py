from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER,CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex
from spacy.gold import biluo_tags_from_offsets
import re
import spacy
from spacy.matcher import Matcher
import srsly
from spacy.util import minibatch, compounding
from agData import *
import random
from pathlib import Path

path_to_pretrained_weights="/Users/gonsongo/Desktop/research/iaa/Projects/python/IaaAgDataNER/preTrainInput/text.jsonl"

def trainModel(model=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Model loaded.. '%s'" % model)
    else:
        nlp = spacy.blank("en_core_web_lg")  # create blank Language class
        print("Created blank 'en_core_web_lg' model")

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

            # Now that we have our model, we can load in the pretrained weights.
            with open(path_to_pretrained_weights, "rb") as file_:
                nlp.model.tok2vec.from_bytes(file_.read())

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



# The code below is custom to agData. It modifies how the
# parser works to avoid splitting pedigrees

nlp = spacy.load('en_core_web_lg')

# Tell spacy not to split between hyphens
infixes = (
        LIST_ELLIPSES
        + LIST_ICONS
        + [
            #r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[0-9])[+\*^](?=[0-9-])", # Do not split on -
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES),
            r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
            r"(?<=[{a}0-9])[:<>=](?=[{a}])".format(a=ALPHA) # Do not split in /
           #r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA)
        ]
        )
infix_re = compile_infix_regex(infixes)
# Tell spacy not to split between hyphens (-) and slashes (/)
nlp.tokenizer.infix_finditer = infix_re.finditer

# Try to match journal: Crop Science 32(3):828 (1992)
digit_hyphen_re = re.compile(r'\s\(\d\)')
nlp.tokenizer.token_match = digit_hyphen_re.search


'''
doc = nlp("It was selected from the cross Steveland/Luther//Wintermalt")
for token in doc:
    print(token.text)

doc = nlp("It was derived from I1162-19/J-126//WA1245///Steptoe.")
values=[]
for token in doc:
    values.append(token.text)
preTrainData=[{"tokens":values}]
path="/Users/gonsongo/Desktop/research/iaa/Projects/python/IaaAgDataNER/preTrainInput"
srsly.write_jsonl(path+"/text.jsonl", preTrainData)
# --use-vectors to use the vectors from existing English model.

# python3 -m spacy download en_core_web_lg
# python3 -m spacy pretrain  preTrainInput/text.jsonl "en_core_web_lg" preTrainOutput --use-vectors
# python3 -m spacy convert trainData.jsonl --converter jsonl -l en > trainData.json
# python3 -m spacy train en NerModel trainData.json trainData.json --pipeline ner --init-tok2ve preTrainOutput/model999.bin --n-iter 10

# Change --n-iter 1000 in actual implementation
'''

doc = nlp("It was selected from the cross I1162-19/J-126//WA1245///Steptoe")
for token in doc:
    print(token.text)


doc = nlp("The journal is Crop Science 32(3):828 (1992)")

# for token in doc:
#     print(token.text)

indexes = [m.span() for m in re.finditer('[\w|\S]+\s[\w|\S]+\s\([\w|\S]+\)', doc.text, flags=re.IGNORECASE)]
print("\n")
print(indexes)
for (span_start, span_end) in indexes:
    print(doc.text[span_start:span_end])

