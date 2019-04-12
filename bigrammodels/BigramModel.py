from nltk import bigrams
from utilities import *
import json
from collections import defaultdict


class BigramModel():
    """
        Takes all documents from both corpuses, gets all bigram pairs, calculates total occurences and then saves them all into a dictionary
        Dictionary saved into JSON for further processing

        Code for building bigram model was inspired from: https://nlpforhackers.io/language-models/
    """

    def __init__(self):
        with open('corpus.json') as corpus, open('corpus-reuters.json') as corpus_reuters:
            c = json.load(corpus)
            c_r = json.load(corpus_reuters)
            self.complete_set = [
                document for document in c] + [document for document in c_r]

    def build_bigrams(self):
        model = defaultdict(lambda: defaultdict(lambda: 0))
        for document in self.complete_set:
            fulltext = remove_stopwords([lowercase_folding(word)
                                         for word in tokenize_word(document['fulltext']) if word not in string.punctuation and not any(i.isdigit() for i in word) and word != ""])

            for w1, w2 in bigrams(fulltext):
                model[w1][w2] += 1

            for w1 in model:
                total_count = float(sum(model[w1].values()))
                for w2 in model[w1]:
                    model[w1][w2] /= total_count
        with open('bigram_model.json', 'w') as outfile:
            json.dump(model, outfile, ensure_ascii=False, indent=4)
        return model
