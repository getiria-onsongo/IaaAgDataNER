import spacy
import pandas as pd


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

def expand_adj_spans():
    nlp = spacy.load("en_core_web_sm")
    doc = nlp("beautiful small old Beligum fought the whole world.")

    for ent in doc.ents:
        print("old: " + str(ent.text))
        index = doc[ent.start:ent.end][0].i
        start = get_all_adj(doc, ent, index)
        first_tok = doc[start]
        ent = doc[first_tok.i:ent.end]
        print("new: " + str(ent))

def process_csv(f):
    df = pd.read_csv(f)
    counter = 1
    for col_name in df.columns:
        if col_name != 'Sentences':
            ent_split = df[col_name].str.split(' ', expand=True)
            ent_split_df = pd.DataFrame()
            name1 = 'ent'+str(counter)+' ind1'
            name2 = 'ent'+str(counter)+' ind2'
            name3 = 'ent'+str(counter)+' label'
            ent_split_df[[name1, name2, name3]] = ent_split
            ent_split_df[name1] = ent_split_df[name1].apply(pd.to_numeric, errors='ignore')
            ent_split_df[name2] = ent_split_df[name2].apply(pd.to_numeric, errors='ignore')

            df = df.drop(col_name, axis=1)
            df[name1] = ent_split_df[name1]
            df[name2] = ent_split_df[name2]
            df[name3] = ent_split_df[name3]
            counter = counter + 1
    print(df)
    df.to_csv('processed.csv', index=False)
