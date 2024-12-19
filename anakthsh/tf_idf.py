# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 22:49:29 2024

@author: User
"""

import math
import json
from pre_processing import preprocess_text
from web_scrapper import save_data_to_json

def load_tf_idf():
    with open("all_wikipedia_tf_idf.json", encoding="UTF-8") as f:
        data = json.load(f)
    return data

def tf_idf_order_all(index, documents):
    all_terms = dict()
    for term in index:
        tfs = tf_idf_order(term, index, documents)
        for value in tfs:
            if not all_terms.get(term):
                all_terms[term] = list()
            all_terms[term].append([value[1], value[2]])
    save_data_to_json("all_wikipedia_tf_idf.json",all_terms)
    return all_terms
        

def tf_idf_order(term, index, documents):
    if not index.get(term):
        return
    temp = list()
    num_docs = set(index[term])
    temp = [(term, i, tf_idf(term, index, i, documents)) for i in num_docs]
    temp = sorted(temp, key=lambda item: (item[2]), reverse=True)
    return temp

def tf_idf(term, index, doc_num, documents):
    tf = term_frequency(term, index, doc_num, documents)
    idf = inv_doc_frequency(term, index, documents)
    result = tf * idf
    return result
    

def inv_doc_frequency(term, index, documents):
    if not index.get(term):
        return
    num_docs = len(documents)
    num_term_docs = len(set(index[term]))
    idf = math.log(num_docs / num_term_docs, 2)
    return idf
    

def load_index():
    with open("all_wikipedia_index.json", encoding="UTF-8") as f:
        data = json.load(f)
    return data

def load_data():
    with open("all_wikipedia_data.json", encoding="UTF-8") as f:
        data = json.load(f)
    return data

def term_frequency(term, index, doc_num, documents):
    if not index.get(term):
        return
    if len(documents) < doc_num:
        return
    result = 0
    for doc in index[term]:
        if doc == doc_num:
            result = result + 1
    words = 0
    for paragraph in documents[doc_num]['content']:
        tokens = preprocess_text(paragraph)
        words = words + len(tokens)
    result = result/words
    return result

def main():
    index = load_index()
    documents = load_data()
    # print(term_frequency("repeated", index, 0, documents))
    # print(inv_doc_frequency("repeated", index, documents))
    # print(tf_idf("repeated", index, 0, documents))
    # print(tf_idf_order("repeated", index, documents))
    tf_idf_order_all(index, documents)
    # print(tf_idf_order_all(index, documents)['mathematics'])
    return

