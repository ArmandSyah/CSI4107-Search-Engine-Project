from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from scipy.sparse import csr_matrix, lil_matrix
import string
import re
import pandas as pd
import numpy as np
import json
from collections import Counter

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


class KNearestNeighboursClassifier():
    """
        Implementation of kNN. Used to classify the articles without a topic label
        Uses articles with topic as the training set, and the articles without for the test set
        Creates 2 json files, 1 with both the old labeled articles and new labeled articles combined, and
        another for just the updated articles

        KNN code inspired from https://appliedmachinelearning.blog/2018/01/18/conventional-approach-to-text-classification-clustering-using-k-nearest-neighbor-k-means-python-implementation/
    """

    def __init__(self):
        with open('corpus-reuters.json') as corpus:
            corpus_reuters = json.load(corpus)
            self.training_set = [
                article for article in corpus_reuters if article["topic"] != ""]
            self.test_set = [
                article for article in corpus_reuters if article["topic"] == ""]
            self.true_topic_labels = list(
                set(article["topic"] for article in corpus_reuters if article["topic"] != ""))
            self.numeric_topic_labels = {
                label: index for index, label in enumerate(self.true_topic_labels)}

    def process(self):
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(
            [clean(corpus["fulltext"]) for corpus in self.training_set])
        y_training = np.fromiter([
            self.numeric_topic_labels[corpus["topic"]] for corpus in self.training_set], int)
        modelknn = KNeighborsClassifier(n_neighbors=5, metric="euclidean")
        modelknn.fit(X, y_training)

        test_set_lookup = {article["doc_id"]: clean(
            article["fulltext"]) for article in self.test_set}
        Test = vectorizer.transform(test_set_lookup.values())
        predicted_labels_knn = modelknn.predict(Test)

        updated_articles = []
        for index, article in enumerate(self.test_set):
            article["topic"] = self.true_topic_labels[np.int(
                predicted_labels_knn[index])]
            updated_articles.append(article)

        with open('updated_corpus_reuters_knn.json', 'w') as outfile:
            json.dump(self.training_set + updated_articles,
                      outfile, ensure_ascii=False, indent=4)

        with open('set_of_updated_reuters_articles_knn.json', 'w') as outfile:
            json.dump(updated_articles,
                      outfile, ensure_ascii=False, indent=4)


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word)
                          for word in punc_free.split())
    processed = re.sub(r"\d+", "", normalized)
    return processed
