import sys
from preprocessing import UOPreprocessing, ReutersPreprocessing
from dictionary import dictionary
from invertedindex import InvertedIndex
from timeit import default_timer as timer


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
    inv_ind = inverted_index.make_inverted_index()
    print("finished setting up inverted index")
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
    else:
        print("invalid args")
