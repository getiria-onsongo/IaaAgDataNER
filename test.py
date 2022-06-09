import spacy

def get_all_adj(doc, ent, index):
    new_start = index
    i = index
    while i >= 1:
        i = i - 1
        if doc[i].pos_ == "ADJ":
            new_start = i
        else:
            break
    return new_start

nlp = spacy.load("en_core_web_sm")
doc = nlp("beautiful small old Beligum fought the whole world.")

for ent in doc.ents:
    print("old: " + str(ent.text))
    index = doc[ent.start:ent.end][0].i
    start = get_all_adj(doc, ent, index)
    first_tok = doc[start]
    ent = doc[first_tok.i:ent.end]
    print("new: " + str(ent))
