import sys
from preprocessing import UOPreprocessing, ReutersPreprocessing
from dictionary import dictionary
from invertedindex import InvertedIndex
from vectorspacemodel import VectorSpaceModel
from bigrammodels import BigramModel
from thesaurus import Thesaurus
from textcategorization import knearestneighbours, naivebayes
from timeit import default_timer as timer
import pickle


def setupcorpus():
    print("setting up corpi")
    proc, reut = UOPreprocessing.UOPreprocessing(
    ), ReutersPreprocessing.ReutersPreprocessing()
    proc.preprocess_collections()
    reut.preprocess_collections()
    print("finished setting up corpi")


def setupdict():
    start = timer()
    print("setting up dict")
    uo_dict = dictionary.Dictionary()
    uo_dict.make_dictionary()
    print("finished setting up dict")
    end = timer()
    print(f"{end - start} seconds")


def setupinvertedindex():
    start = timer()
    print("setting up inverted index")
    inverted_index = InvertedIndex.InvertedIndex()
    inverted_index.make_inverted_index()
    print("finished setting up inverted index")
    end = timer()
    print(f"{end - start} seconds")


def makelist():
    topic_choice = []
    with open('all-topics-strings.lc.txt') as topics:
        for topic in topics:
            topic_choice.append((topic.rstrip(), topic.rstrip()))

    with open('list_of_topics.pickle', 'wb') as fp:
        pickle.dump(topic_choice, fp)


def makebigrammodel():
    start = timer()
    print("setting up bigram model")
    bigram = BigramModel.BigramModel()
    bigram.build_bigrams()
    print("finished setting up bigram model")
    end = timer()
    print(f"{end - start} seconds")


def make_doc_term():
    start = timer()
    print("setting up doc_term_table")
    thesaurus = Thesaurus.Thesaurus()
    thesaurus.build_doc_term_table()
    print("finished setting up doc_term_table")
    end = timer()
    print(f"{end - start} seconds")


def make_thesaurus():
    start = timer()
    print("setting up thesaurus")
    thesaurus = Thesaurus.Thesaurus()
    thesaurus.build_jaccard_word_pair_table()
    print("finished setting up thesaurus")
    end = timer()
    print(f"{end - start} seconds")


def make_knn():
    start = timer()
    print("setting up k nearest neighbours topics")
    c = knearestneighbours.KNearestNeighboursClassifier()
    c.process()
    print("finished setting up naive bayes topics")
    end = timer()
    print(f"{end - start} seconds")


def make_nb():
    start = timer()
    print("setting up naive bayes topics")
    c = naivebayes.NaiveBayesClassifier()
    c.process()
    print("finished setting up naive bayes topics")
    end = timer()
    print(f"{end - start} seconds")


if __name__ == "__main__":
    args = sys.argv
    if args[1] == "corpus":
        setupcorpus()
    elif args[1] == "dict":
        setupdict()
    elif args[1] == "index":
        setupinvertedindex()
    elif args[1] == "list":
        makelist()
    elif args[1] == "bigram":
        makebigrammodel()
    elif args[1] == "docterm":
        make_doc_term()
    elif args[1] == "thesaurus":
        make_thesaurus()
    elif args[1] == "knn":
        make_knn()
    elif args[1] == "nb":
        make_nb()
    else:
        print(f"invalid args: {args[1]}")
