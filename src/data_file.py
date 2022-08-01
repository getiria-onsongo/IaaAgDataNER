import os
from dataclasses import dataclass

"""
Extracted MedaCy wrapper class for text files in MedaCy datasets. MedaCy datasets are needed to calculate the metrics using inter_dataset_agreement for k-fold cross validation.
"""

@dataclass
class DataFile:
    """
    DataFile wraps all relevant information needed to manage a text document and it's corresponding annotation. Specifically,
    a Datafile keeps track of the filepath of the raw text, annotation file, and metamapped file for each document.
    :ivar file_name: the name of the file being represented
    :ivar txt_path: the text document corresponding to this file
    :ivar ann_path: the annotations of the text document
    :ivar metamapped_path: the metamap file
    """
    file_name: str
    txt_path: os.PathLike
    ann_path: os.PathLike
    metamapped_path: os.PathLike = None
