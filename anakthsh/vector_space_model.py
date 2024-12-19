# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 11:14:53 2024

@author: User
"""
from numpy.linalg import norm
from web_scrapper import from_json_to_str
from inverted_index import create_index
import json
from tf_idf import tf_idf
# from matplotlib import cm
# import matplotlib.pyplot as plt
# import pandas as pd
from web_scrapper import save_data_to_json
from tf_idf import load_index
import numpy as np
from tf_idf import load_data

def cosine_similarity(query, index, documents):
    matrix = query_to_vector(query, index, documents)
    sizey = matrix.shape[0]
    B = matrix[sizey-1]
    A = matrix[0:sizey-1]
    cosine = np.dot(A,B)/(norm(A, axis=1)*norm(B))
    print("Cosine Similarity:\n", cosine)
    return cosine
    
def load_matrix():
    with open("all_wikipedia_matrix.json", encoding="UTF-8") as f:
        data = json.load(f)
    return data    

def query_to_vector(query, index, documents):
    lisdex = keys_to_list(index)
    sizex = len(lisdex)
    pack = {"title": "Query","content": [query]}
    documents.append(pack)
    index = create_index(from_json_to_str(documents))
    # print(documents)
    sizey = len(documents)
    matrix = np.zeros([sizey, sizex], dtype=float)
    for term in lisdex:
        indx = lisdex.index(term)
        szdoc = range(sizey)
        for doc_num in szdoc:
            matrix[doc_num, indx] = tf_idf(term, index, doc_num, documents)
        # for docnum in index[term]:
        #     indx = lisdex.index(term)
        #     matrix[docnum, indx] = matrix[docnum, indx] + 1.0
            
    # print(matrix[sizey-1])
    # print_matrix(matrix, lisdex, docs_to_list(documents))
    save_data_to_json("all_wikipedia_query.json",matrix.tolist())
    return matrix
    
# def print_matrix(matrix, lisdex, lisdoc):
#     dtfrm = pd.DataFrame(matrix, index=lisdoc, columns=lisdex)
#     print(dtfrm)
    
    
#     # make data
#     Z = np.repeat(matrix, 1000, axis=0)
#     X, Y = np.meshgrid(range((matrix.shape[0])), range((matrix.shape[1])))
#     Z = Z.transpose()
    
#     # plot
#     fig, ax = plt.subplots()
    
#     ax.imshow(Z, origin='lower', cmap=cm.pink)
#     plt.savefig("term_document_matrix.pdf")
#     plt.show()

#     # # Plot the surface
#     # X, Y = np.meshgrid(range(len(lisdex)), range(len(lisdoc)))
#     # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
#     # ax.plot_surface(X, Y, matrix, cmap=cm.Reds)
#     # plt.savefig("term_document_matrix.pdf")
#     # plt.show()

def docs_to_list(documents):
    res = [ i['title'] for i in documents]
    return(res)

def term_document_matrix(lisdex, documents, index):
    sizex = len(lisdex)
    sizey = len(documents)
    matrix = np.zeros([sizey, sizex], dtype=float)
    for term in lisdex:
        indx = lisdex.index(term)
        szdoc = range(sizey)
        for doc_num in szdoc:
            matrix[doc_num, indx] = tf_idf(term, index, doc_num, documents)
        # for docnum in index[term]:
        #     indx = lisdex.index(term)
        #     matrix[docnum, indx] = matrix[docnum, indx] + 1.0
            
    # print_matrix(matrix, lisdex, docs_to_list(documents))
    save_data_to_json("all_wikipedia_matrix.json",matrix.tolist())
    
    return matrix

def keys_to_list(index):
    lisdex = list(index.keys())
    lisdex = sorted(lisdex)
    return lisdex
    
def main():
    index = load_index()
    docum = load_data()
    # matrix = load_matrix()
    # print(keys_to_list(index)[0:5])
    # lisdex = keys_to_list(index)
    # print_matrix(np.array(matrix), lisdex, docs_to_list(docum))
    # print(term_document_matrix(lisdex, docum, index))
    cosine_similarity("mathematics two", index, docum)
    

main()