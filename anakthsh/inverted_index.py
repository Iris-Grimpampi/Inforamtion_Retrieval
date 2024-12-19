from collections import defaultdict
from pre_processing import preprocess_text

def create_index(text_content):
    inverted_index = defaultdict(list)  # Το ευρετήριο αποθηκεύει λέξεις και τις θέσεις τους
    for position, paragraph in enumerate(text_content):
        tokens = preprocess_text(paragraph)
        for token in tokens:
            inverted_index[token].append(position)
    return inverted_index