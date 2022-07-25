from pathlib import Path
import typer
import spacy
from spacy.tokens import DocBin


"""
From https://github.com/explosion/projects/blob/v3/experimental/ner_spancat/
"""

def convert_to_span(loc: Path, lang: str, span_key: str):
    """
    Set the NER data into the doc.spans, under a given key.

    The SpanCategorizer component uses the doc.spans, so that it can work with
    overlapping or nested annotations, which can't be represented on the
    per-token level.
    """
    nlp = spacy.blank(lang)
    docbin = DocBin().from_disk(loc)
    docs = list(docbin.get_docs(nlp.vocab))
    for doc in docs:
        doc.spans[span_key] = list(doc.ents)
    DocBin(docs=docs).to_disk(loc)
