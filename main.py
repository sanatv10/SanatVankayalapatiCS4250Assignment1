# AUTHOR: Sanat Vankayalapati
# FILENAME: main.py
# SPECIFICATION: . The purpose of the program is to demonstrate a method of information retrieval. One of the most common types of information retrieval is tf-idf. The goal of the program is to read through a CSV file with text phrases (each row of the CSV file representing an individual document) and print out the tf-idf document term matrix.
# FOR: CS 4250- Assignment #1
# TIME SPENT: 2 days

import csv
from math import log10
from collections import defaultdict


documents = []
with open('collection.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i > 0:
            documents.append(row[0])


stopWords = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which",
    "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by",
    "for", "with", "about", "against", "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under",
    "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all",
    "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don",
    "should", "now"
}


steeming = {
    "cats": "cat", "dogs": "dog", "loves": "lov", "love": "lov", "dog": "dog", "cat": "cat"
}


def preprocess(document):
    document = document.lower()
    words = document.split()
    return [steeming.get(word[:-1] if word.endswith('s') else word, word)
            for word in words if word not in stopWords]


terms = []
for document in documents:
    terms.extend(preprocess(document))
terms = sorted(set(terms))


def compute_tf(documents):
    tf_list = []
    for doc in documents:
        word_count = defaultdict(int)
        words = preprocess(doc)
        total_terms = len(words)
        for word in words:
            word_count[word] += 1
        tf_list.append({word: count / total_terms for word, count in word_count.items()})
    return tf_list

def compute_df(documents):
    df = defaultdict(int)
    for doc in documents:
        unique_words = set(preprocess(doc))
        for word in unique_words:
            df[word] += 1
    return df

def compute_tfidf(tf_list, df, total_docs):
    tfidf_list = []
    for tf in tf_list:
        tfidf = {}
        for word, tf_value in tf.items():
            idf = log10(total_docs / df[word])
            tfidf[word] = tf_value * idf
        tfidf_list.append(tfidf)
    return tfidf_list


tf_list = compute_tf(documents)
df = compute_df(documents)
total_docs = len(documents)


docTermMatrix = compute_tfidf(tf_list, df, total_docs)


header = "\t".join(terms)
print(f"\t{header}")

for i, tfidf in enumerate(docTermMatrix):
    row = [tfidf.get(term, 0) for term in terms]
    print(f"Doc {i+1}:\t" + "\t".join(f"{value:.2f}" for value in row))


