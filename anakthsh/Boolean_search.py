# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 13:34:33 2024

@author: User
"""
import json
# from pre_processing import preprocess_text 
# import ast
import re   

def set_evaluation(str_search, index, doc_size):
    
    list_search = re.split('[., ]',str_search)
    
    prev_flag = False
    prev_not = False
    list_res = []
    for ind, word in enumerate(list_search):
        if (not index.get(word)) and (word not in ["and","or","not"]):
            prev_flag = True
            continue
        if word in ["not"]:
            prev_not = True
            tmp_set = set(index[list_search[ind+1]])
            tmp_set = set(range(doc_size)) - tmp_set
            list_res.append(str(tmp_set))
        elif word not in ["and","or","not"]:
            if prev_not:
                prev_not = False
            else:
                tmp_set = set(index[list_search[ind]])
                list_res.append(str(tmp_set))
        elif word in ["and"]:
            if prev_flag:
                prev_flag = False
            else:
                list_res.append("&")
        elif word in ["or"]:
            if prev_flag:
                prev_flag = False
            else:
                list_res.append("|")
            
        tmp_set = set()
        # print(" ".join(list_res))
            
    resstr = " ".join(list_res)
    # print(resstr)
    # resstr = resstr.replace("and", "&")
    # resstr = resstr.replace("or", "|")
        
    return list(eval(resstr))
    
def boolean_search(terms):
    
    with open("all_wikipedia_data.json", encoding="UTF-8") as f:
        data = json.load(f)
    with open("all_wikipedia_index.json", encoding="UTF-8") as f:
        index = json.load(f)
    
    results = set_evaluation(terms, index, len(data))
            
    return(results)
    
# def order_boolean(terms):
#     import re
#     terms_split = re.split('[., ]',terms)
#     print(terms_split)
#     boolean_precedence = dict()
#     boolean_precedence['not'] = list()
#     boolean_precedence['and'] = list()
#     boolean_precedence['or'] = list()
#     for i in range(len(terms_split)):
#         if(terms_split[i] == "not"):
#             boolean_precedence['not'].append((terms_split[i+1]))
#     terms_split = [temp for temp in terms_split if temp not in 'not']
#     for i in range(len(terms_split)):
#         if(terms_split[i] == "and"):
#             boolean_precedence['and'].append((terms_split[i-1]))
#             boolean_precedence['and'].append((terms_split[i+1]))
#     terms_split = [temp for temp in terms_split if temp not in 'and']
#     for i in range(len(terms_split)):
#         if(terms_split[i] == "or"):
#             boolean_precedence['or'].append((terms_split[i-1]))
#             boolean_precedence['or'].append((terms_split[i+1]))
#     terms_split = [temp for temp in terms_split if temp not in 'or']
#     return(boolean_precedence)

# def boolean_praxis(search,  precedence):
#     with open("all_wikipedia_index.json", encoding="UTF-8") as f:
#         index = json.load(f)
#     maxim = 0
#     for term in index:
#         for pointer in index[term]:
#             if maxim < int(pointer):
#                 maxim = pointer
#     for term in precedence['not']:
#         if search.get(term):
#             print(set(range(maxim+1)) - set(search[term]))
#             search[term] = (set(range(maxim+1)) - set(search[term]))
            
#     for i in range(0,len(precedence['and']),2):
#         term1 = precedence['and'][i]
#         term2 = precedence['and'][i+1]
#         if search.get(term1) and search.get(term2):
#             print(set(search[term1]) & set(search[term2]))
#             search[term1] = (set(search[term1]) & set(search[term2]))

            
#     for i in range(0,len(precedence['or']),2):
#         term1 = precedence['or'][i]
#         term2 = precedence['or'][i+1]
#         if search.get(term1) and search.get(term2):
#             print(set(search[term1]) | set(search[term2]))
#             search[term1] = (set(search[term1]) | set(search[term2]))



def main():
    terms = "love and not mathematics or not 10 and two or bilinear"
    # print(boolean_search(terms))
    # print(order_boolean(terms))
    # boolean_praxis(boolean_search(terms), order_boolean(terms))
    print(boolean_search(terms))
    
main()
