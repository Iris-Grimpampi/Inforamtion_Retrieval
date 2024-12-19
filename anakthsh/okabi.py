from inverted_index import *
from nltk.text import Text
from pre_processing import preprocess_text
import math
import json
from tf_idf import inv_doc_frequency
from tf_idf import term_frequency
from miscellaneous import from_num_to_title

# Define bm25 function
def bm25(index: dict, documents: list[dict], query: str) -> dict:
    """Compute the BM25 score for each document in the index."""
    K1 = 1.2
    K3 = 1.2
    B = 0.75

    query_words = preprocess_text(query)  # Process query words

    # Calculate the average document length
    avg_doc_len = sum(len(preprocess_text("\n".join(doc['content']))) for doc in documents) / len(documents)

    scores = {}
    no_index_terms = []  # To track terms that don't exist in the index

    for doc_id, doc in enumerate(documents):
        rsv = 0.0
        doc_len = len(preprocess_text("\n".join(doc['content'])))  # Length of the current document

        for word in query_words:
            # Skip word if it doesn't exist in the index
            if word not in index:
                no_index_terms.append(word)
                continue

            idf = inv_doc_frequency(word, index, documents)  # IDF for the word
            tf_td = term_frequency(word, index, doc_id, documents)  # Term frequency for the word in the document
            tf_qt = query_words.count(word)  # Term frequency in the query

            if idf == 0 or tf_td == 0:  # Skip if IDF or TF in document is zero
                continue

            numerator = ((K1 + 1) * tf_td) * ((K3 + 1) * tf_qt)
            denominator = (K1 * ((1 - B) + B * (doc_len / avg_doc_len)) + tf_td) * (K3 + tf_qt)

            rsv += idf * numerator / denominator

        if rsv > 0:
            scores[doc_id] = rsv

    # Sort documents by score in descending order and return
    sorted_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    # If there were terms in the query not in the index, show a warning message
    if no_index_terms:
        print(f"Warning: The following query terms were not found in the index: {', '.join(no_index_terms)}")

    return {doc_id: score for doc_id, score in sorted_docs}

# Define search function
def okabi_search(index, documents, query: str) -> set:
    """Search the index with the query and return a sorted set of document IDs."""
    # print("Index:", index)  # Debugging line to check the structure of the index

    scores = bm25(index, documents, query)

    # Return the set of document IDs sorted by score
    return set(scores.keys())

# Import the functions from tf_idf.py after function definitions
from tf_idf import load_index, load_data

# Load the index and documents
index = load_index()
documents = load_data()

# Example search query
query = "ssdsds mathematics two"
for i in okabi_search(index, documents, query):
    print(from_num_to_title(i, documents))