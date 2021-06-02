#!/bin/env python3
import os
def rawJsonToSpacyJson(dir=None, fileSuffix=".json", outputFileName=None):
    """Add docstring"""

    dir = "/Users/gonsongo/Desktop/research/iaa/Projects/python/IaaAgDataNER/Data/test"
    path = os.walk(dir)
    for root, directories, files in path:
        for name in files:
            if name.endswith(fileSuffix):
                print(os.path.join(root, name))
        for name in directories:
            if name.endswith(fileSuffix):
                print(os.path.join(root, name))