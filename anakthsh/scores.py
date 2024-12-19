# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 17:15:53 2024

@author: User
"""
from tf_idf import load_index
from tf_idf import load_data
from Boolean_search import boolean_search
from vector_space_model import cosine_similarity
from okabi import okabi_search


# Recall Precision and F-score

def f_score(retrieved: list, relevant: list):
    precision, recall = retrieved_relevant_to_precision_recall(retrieved, relevant)
    num_of_values = 2
    if precision == 0 or recall == 0:
        return 0
    mid_sum = 1/precision +1/recall
    mean = num_of_values/mid_sum
    return mean

def retrieved_relevant_to_precision_recall(retrieved: list, relevant: list): 
    #four is: 
        #1 retrieved and relevant (true positive)
        #2 retrieved and irrelevant (false positive)
        #3 not retrieved and relevant (false negative)
        #4 not retrieved and irrelevant (true negative)
    blue = set(relevant)
    green = set(retrieved)
    gray = blue & green
    # print("relevant: ", blue)
    # print("retrieved: ", green)
    # print("true positives: ",gray)
    if len(green) == 0 or len(blue) == 0:
        return (0, 0)
    precision = len(gray) / len(green)
    recall = len(gray) / len(blue)
    return precision, recall

def main():
    index = load_index()
    docum = load_data()
    
    query = "blah blah blah mathematics two love expressed obtained values"
    querybool = "blah and blah and mathematics and two and love and expressed and obtained and values"
    # querybool = "blah and blah or not mathematics and not two or love and expressed and obtained or values"
    relevant = [0, 1] #change to the relevant documents
    retrieved = list()
    
    #methods
    print("Boolean method")    
    retrieved = boolean_search(querybool)
    precision, recall = retrieved_relevant_to_precision_recall(retrieved, relevant)
    fscore = f_score(retrieved, relevant)
    print("Precision: ",precision)
    print("Recall: ",recall)
    print("F-score: ",fscore)
    
    print("VSM method")    
    retrieved = cosine_similarity(query, index, docum)
    precision, recall = retrieved_relevant_to_precision_recall(retrieved, relevant)
    fscore = f_score(retrieved, relevant)
    print("Precision: ",precision)
    print("Recall: ",recall)
    print("F-score: ",fscore)
    
    print("Okabi method")    
    retrieved = okabi_search(index, docum, query)
    precision, recall = retrieved_relevant_to_precision_recall(retrieved, relevant)
    fscore = f_score(retrieved, relevant)
    print("Precision: ",precision)
    print("Recall: ",recall)
    print("F-score: ",fscore)
    
    
main()