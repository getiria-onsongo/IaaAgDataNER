#!/bin/env python3
from agParse import *

output_dir = "/Users/gonsongo/Desktop/research/iaa/Projects/python/IaaAgDataNER/agdataNew"
# trainModel(None, output_dir, 100)
print("Loading trained model", output_dir)
agdata_nlp = spacy.load(output_dir)
agdata_nlp.add_pipe(compound_trait_entities, after='ner')

print("Component in pipeline")
print(agdata_nlp.pipe_names)

test1 = 'The cross Triumph/Victor was published in Journal of American Society of Agronomy 33:252 (1941).'
doc = agdata_nlp(test1)
print("\nTest1=",test1)
print("Entities:")
for ent in doc.ents:
        print(ent.text,ent.label_)
test2 = '''
Kold is a six-rowed winter feed barley and it was published in Crop Science 25:1123 (1985).
It was published in Crop Science 9(4):521 (1969).
It was published in Crop Science 41:265-266 (2001).
It was published in Crop Science 30(2): 421 (1990).
It was published in Crop Science 42:665-666 (2002).
It was selected from the cross Robust/6/Glenn/4/Nordic//Dickson/Trophy/3/Azure/5/Glenn/Karl.
It was published in Journal of American Society of Agronomy 33:252 (1941).'''

doc = agdata_nlp(test2)
print("\nTest2=",test2)
print("Entities:")
for ent in doc.ents:
        print(ent.text,ent.label_)

test3='Triumph/Victor was published in Science 30(2): 421 (1990).'
doc = agdata_nlp(test3)
print("\nTest3=",test3)
print("Entities:")
for ent in doc.ents:
        print(ent.text,ent.label_)



