from .PreprocessingBase import PreprocessingBase
from bs4 import BeautifulSoup
import requests
import json
import re
import os
from utilities import tokenize_sentence


class ReutersPreprocessing(PreprocessingBase):

    def __init__(self):
        super().__init__()
        self.reutersfiles = os.path.join(os.getcwd(), "reutersdataset")

    def preprocess_collections(self):
        for filename in os.listdir(self.reutersfiles):
            with open(os.path.join(self.reutersfiles, filename), 'r') as reuterfile:
                data = reuterfile.read()
                soup = BeautifulSoup(data, "html.parser")
                articles = soup.find_all('reuters')

                for index, article in enumerate(articles, 1):
                    title = article.find('title').text if article.find(
                        'title') is not None else ""
                    description = article.find('body').text if article.find(
                        'body') is not None else ""
                    if description == "":
                        continue
                    excerpt = tokenize_sentence(description.strip())[
                        0] if description is not None and description != "" else ''

                    topics = article.find('topics').find_all("d")[0].text if article.find(
                        'topics').find("d") is not None else ""
                    new_document = self.Document(f'{filename}-article #{index}', title, description.strip(
                    ) if description is not None else '', excerpt, topics)
                    self.uniform_collections.append(new_document)

        uniform_dicts = [uniform_collection._asdict()
                         for uniform_collection in self.uniform_collections]

        with open('corpus-reuters.json', 'w') as outfile:
            json.dump(uniform_dicts, outfile, ensure_ascii=False, indent=4)
