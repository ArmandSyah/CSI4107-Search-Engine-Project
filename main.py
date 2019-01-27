from preprocessing import UOPreprocessing
from dictionary import dictionary
import json

if __name__ == "__main__":
    proc = UOPreprocessing.UOPreprocessing()
    proc.preprocess_collections()

    uo_dict = dictionary.Dictionary()
    uo_dict.make_dictionary()

    with open('dictionary.json', 'w') as outfile:
        uo_dict_lists = {k: list(v) for (k, v) in uo_dict.dict.items()}
        json.dump(uo_dict_lists, outfile, ensure_ascii=False, indent=4)
