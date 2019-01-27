from .PreprocessingBase import PreprocessingBase
from bs4 import BeautifulSoup
import requests
import json


class UOPreprocessing(PreprocessingBase):
    def __init__(self):
        super().__init__()
        self.url = 'https://catalogue.uottawa.ca/en/courses/csi/'

    def preprocess_collections(self):
        try:
            results = requests.get(self.url)
            results.raise_for_status()
        except requests.exceptions.RequestException as r:
            print(r)
            print(f"Can't make get request with this URL: {self.url}")
            raise

        soup = BeautifulSoup(results.text, 'html.parser')
        courseblocks = soup.find_all('div', attrs={'class': 'courseblock'})

        for index, courseblock in enumerate(courseblocks, 1):
            course_title = courseblock.find(
                'p', attrs={'class': 'courseblocktitle'})
            course_description = courseblock.find(
                'p', attrs={'class': 'courseblockdesc'})
            new_document = self.Document(
                f'CSI-{index}', course_title.text, course_description.text.strip() if course_description is not None else '')
            self.uniform_collections.append(new_document)

        uniform_dicts = [uniform_collection._asdict()
                         for uniform_collection in self.uniform_collections]

        with open('corpus.json', 'w') as outfile:
            json.dump(uniform_dicts, outfile, ensure_ascii=False, indent=4)
