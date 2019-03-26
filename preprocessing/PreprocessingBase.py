from abc import ABC, abstractmethod
from collections import namedtuple

# Module 1 - Preprocessing


class PreprocessingBase(ABC):

    """Base class of for all text collection preprocessing

    All preprocessing classes inherit from this abstract class, formatting the preprocessed text in
    the following structure, regardless of how the class performs its preprocessing (scraping websites, ect.)

    {
        'doc_id': CSI-1
        'title': 'Example Title'
        'fulltext': 'this is fulltext'
        'excerpt': 'excerpt'
    }

    This class was inspired by https://www.python-course.eu/python3_abstract_classes.php
    """

    def __init__(self):
        self.Document = namedtuple(
            "Document", "doc_id title fulltext excerpt topic")
        self.uniform_collections = []
        super().__init__()

    @abstractmethod
    def preprocess_collections(self):
        pass
