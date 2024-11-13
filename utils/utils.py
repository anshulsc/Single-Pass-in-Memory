#! /usr/bin/env python3
# coding: utf-8

import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(os.path.realpath(THIS_DIR))

word_tokenize = word_tokenize
stopwords = set(stopwords.words("english"))
ps = PorterStemmer()

ROOT_DIR = './'

def stem_index(index):
    """
    We will use this method to convert all index keys to lowercase, which will produce more consistent results when we
    conduct queries.
    Note: This is only used for the queries. The index that appears in the index.txt file hasn't been modified.

    :param index: dictionary containing terms and the postings in which they appear.

    :return: index with all keys stemmed, making sure the postings combine as well. For example:
    {'hello': [1, 2], 'Hello': [1, 3], 'HELLO': [2, 3, 5]} would return a dictionary of: {'hello': [1, 2, 3, 5]}.
    """
    new_index = {}
    for k, v in index.items():
        if ps.stem(k) not in new_index.keys():
            new_index[ps.stem(k)] = index[k]
        else:
            new_index[ps.stem(k)] = new_index[ps.stem(k)] + index[k]

    return new_index