#!/bin/env python3

import os
import shutil
import pytest
import subprocess
from nerTraining import trainModel
from checkAccuracy import *

train_data = '[{"doc": "test", "url": "No source", "chunk": "1", "sentences": {"Eight-Twelve is a six-rowed winter feed barley.": {"entity 1": {"start": 0, "end": 12, "label": "CVAR"}, "entity 2": {"start": 18, "end": 27, "label": "TRAT"}, "entity 3": {"start": 28, "end": 34, "label": "TRAT"}, "entity 4": {"start": 35, "end": 39, "label": "TRAT"}, "entity 5": {"start": 40, "end": 46, "label": "CROP"}}, "Maja is a six-rowed winter feed barley.": {"entity 1": {"start": 0, "end": 4, "label": "CVAR"}, "entity 2": {"start": 10, "end": 19, "label": "TRAT"}, "entity 3": {"start": 20, "end": 26, "label": "TRAT"}, "entity 4": {"start": 27, "end": 31, "label": "TRAT"}, "entity 5": {"start": 32, "end": 38, "label": "CROP"}}}}, {"doc": "test", "url": "No source", "chunk": "2", "sentences": {"2   AC METCALFE  AC Metcalfe is a two-rowed spring malting barley.": {"entity 1": {"start": 17, "end": 28, "label": "CVAR"}, "entity 2": {"start": 34, "end": 43, "label": "TRAT"}, "entity 3": {"start": 44, "end": 50, "label": "TRAT"}, "entity 4": {"start": 51, "end": 58, "label": "TRAT"}, "entity 5": {"start": 59, "end": 65, "label": "CROP"}}}}]\n'

train_file, mdir = "/tmp/sample_nlp_data.json", "/tmp/sample_nlp_model"

#
# NOTE: look into get pytest.fixtures working. Without it, there is a lot
# of overhead checking to create it and then destroying it after the last one
#

def setup_model():
    """Setup a simple NLP model and a training file with errors"""

    fo = open(train_file, "w")
    fo.write(train_data)
    fo.close()
    trainModel(None, train_file, mdir, 100)

def test_overlap():
    """Generate an inexact match with an overlap to the original model"""
    # NOTE: alter orig data so that we induce errors so the NLP
    # makes the same prediction while the "truth" is changing

    if not os.path.isdir(mdir):
        setup_model()
        
    ovlp_ex = train_data.replace('0, "end": 12', '1, "end": 14')
    ovlp_fname = "/tmp/sample_ovlp_err.json"
    fo = open(ovlp_fname, "w")
    fo.write(ovlp_ex)
    fo.close()
    stats_fname = "/tmp/ovlp_stats.tsv"
    check_model_accuracy(ovlp_fname, mdir, stats_fname)
    clear_tally()

    # TODO: make this cleaner without file I/O and Unix commands
    res = subprocess.getoutput(["grep 'CVAR' "+stats_fname+" | grep 'overlap' | cut -f 4"])

    # first condition below ensures we didn't get multiple lines above
    assert res.find("\n") == -1 and res == "33.3"

def test_mislabel():
    """Generate a mislabeled entity and compare to the original model"""

    if not os.path.isdir(mdir):
        setup_model()
        
    mislab_ex = train_data.replace('65, "label": "CROP"', '65, "label": "PATH"')
    mislab_fname = "/tmp/sample_mislab_err.json"
    fo = open(mislab_fname, "w")
    fo.write(mislab_ex)
    fo.close()
    stats_fname = "/tmp/mislab_stats.tsv"
    check_model_accuracy(mislab_fname, mdir, stats_fname)
    clear_tally()

    # TODO: make this cleaner without file I/O and Unix commands
    res = subprocess.getoutput(["grep 'CROP' "+stats_fname+" | grep 'mislabel' | cut -f 4"])

    # first condition below ensures we didn't get multiple lines above
    assert res.find("\n") == -1 and res == "33.3"

def test_falseneg():
    """Generate a false negative entity and compare to the original model"""

    if not os.path.isdir(mdir):
        setup_model()
        
    falseneg_ex = train_data.replace('"entity 2": {"start": 18','"entity 1.5": {"start": 13, "end": 17, "label": "PATH"}, "entity 2": {"start": 18')
    falseneg_fname = "/tmp/sample_fn_err.json"
    fo = open(falseneg_fname, "w")
    fo.write(falseneg_ex)
    fo.close()
    stats_fname = "/tmp/fn_stats.tsv"
    check_model_accuracy(falseneg_fname, mdir, stats_fname)
    clear_tally()

    # TODO: make this cleaner without file I/O and Unix commands
    res = subprocess.getoutput(["grep 'PATH' "+stats_fname+" | grep 'false_neg' | cut -f 4"])

    # first condition below ensures we didn't get multiple lines above
    assert res.find("\n") == -1 and res == "100.0"

def test_falsepos():
    """Generate a false positive entity and compare to the original model"""

    if not os.path.isdir(mdir):
        setup_model()
        
    falsepos_ex = train_data.replace('"entity 4": {"start": 27, "end": 31, "label": "TRAT"}, ', '')
    falsepos_fname = "/tmp/sample_fp_err.json"
    fo = open(falsepos_fname, "w")
    fo.write(falsepos_ex)
    fo.close()
    stats_fname = "/tmp/fp_stats.tsv"
    check_model_accuracy(falsepos_fname, mdir, stats_fname)
    clear_tally()

    # TODO: make this cleaner without file I/O and Unix commands
    res = subprocess.getoutput(["grep 'TRAT' "+stats_fname+" | grep 'false_pos' | cut -f 4"])

    # first condition below ensures we didn't get multiple lines above
    assert res.find("\n") == -1 and res == "11.1"

    if os.path.isdir(mdir):
        shutil.rmtree(mdir)
