import json
from utilities import *


class BooleanRetrievalModel():
    """
        Handles the boolean retrieval model for the search engine
        The optional module, Wildcard Management, has been integrated into this class
        through the build_bigram_index function, which is called from check_permutation, which builds out
        every possible word with a wildcard in it (ex: c*s = corpus, cases, ect.)

        To perform the retrieval, first we process the query, changing it from infix to postfix notation,
        find all permutations of words containing * in them, and then retrieve the doc_ids from the inverted index using the words as keys

        The postfix notation transformation code was modified from http://interactivepython.org/runestone/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html

    """

    def __init__(self, inv_index):
        with open('corpus.json') as corpus:
            c = json.load(corpus)
            self.complete_set = {document['doc_id'] for document in c}
        self.inverted_index = inv_index
        self.boolean_tokens = ["and", "or", "not"]
        self.mode = 'unaltered'

    def retrieve(self, query, mode):
        """
        The main retrieval method the UI will call

        Does preprocess the query a bit, depending on the mode, which is also passed
        in from the UI. Afterwards, transforms query from infix to postfix, and then
        performs the actual retrieval from the inverted index
        """
        query = [lowercase_folding(word)
                 for word in word_tokenize(query) if word not in string.punctuation]
        self.mode = mode

        if mode == 'fully_altered':
            query = normalize(stem(remove_stopwords(
                query)))
        elif mode == 'normalized':
            query = normalize(query)
        elif mode == 'stemmed':
            query = stem(query)
        elif mode == 'stopwords_removed':
            query = remove_stopwords(query)

        query = self.infix_to_postfix(query)
        return self.postfix_retrieval(query)

    def infix_to_postfix(self, query):
        opstack = []
        postfix_list = []
        token_list = query

        for token in token_list:
            if token in self.boolean_tokens:
                opstack.append(token)
            elif token.startswith('('):
                opstack.append(token[0])
                if (len(token) > 1):
                    postfix_list.append(token[1:])
            elif token.endswith(')'):
                if (len(token) > 1):
                    postfix_list.append(token[:-1])
                top_token = opstack.pop()
                while top_token != '(':
                    postfix_list.append(top_token)
                    top_token = opstack.pop()
            else:
                postfix_list.append(token)

        while len(opstack) != 0:
            postfix_list.append(opstack.pop())
        return " ".join(postfix_list)

    def postfix_retrieval(self, postfix_query):
        opstack = []
        querystack = []
        token_list = postfix_query.split()

        for token in token_list:
            if token in self.boolean_tokens:
                opstack.append(token)
            else:
                if '*' in token:
                    permutations = self.check_permutations(token)
                    permutations_query = ' or '.join(permutations)
                    querystack.append(
                        self.retrieve(permutations_query, self.mode))
                else:
                    querystack.append(self.perform_retrieve(token))

        for operation in opstack:
            if operation == 'and':
                if len(querystack) >= 2:
                    queries, querystack = querystack[:2], querystack[2:]
                    operand1, operand2 = queries[0], queries[1]
                    intersect_between = operand1.intersection(operand2)
                    querystack.insert(0, intersect_between)
            elif operation == 'or':
                if len(querystack) >= 2:
                    queries, querystack = querystack[:2], querystack[2:]
                    operand1, operand2 = queries[0], queries[1]
                    union_between = operand1.union(operand2)
                    querystack.insert(0, union_between)
            elif operation == 'not':
                if len(querystack) >= 1:
                    query, querystack = querystack[:1], querystack[1:]
                    difference_between = self.complete_set - query
                    querystack.insert(0, difference_between)

        while(len(querystack) > 1):
            queries, querystack = querystack[:2], querystack[2:]
            operand1, operand2 = queries[0], queries[1]
            intersect_between = operand1.intersection(operand2)
            querystack.insert(0, intersect_between)

        return querystack.pop()

    def perform_retrieve(self, token):
        """
        Check if token is in inverted index
        If yes, return the doc_ids within the inverted index
        Else, return an empty set
        """
        if token in self.inverted_index[self.mode]:
            appearances = self.inverted_index[self.mode][token]
            return set(appearance.doc_id for appearance in appearances)
        return set()

    def check_permutations(self, token):
        """
        In the case where token contains a wildcard ('*'), build a bigram index, then return words based
        on position of wildcard.
        Handles wildcard regardless of position
        """
        bigram_index = build_bigram_index(
            self.inverted_index[self.mode], token)
        permutation_set = set()
        for _, ind_list in bigram_index.items():
            if len(permutation_set) == 0:
                permutation_set.update(ind_list)
            else:
                permutation_set.intersection(ind_list)

        # Post filter steps
        # if the token starts with *, then get all words from the permutation set that end with the portion of token after wild card
        # else if token ends with *, then get all words from the permuation set that start with the portions of token before wild card
        # else split the token on the * and find words that contain all split portions
        if token.startswith('*'):
            return [k for k in permutation_set if k.endswith(token[1:])]
        elif token.endswith('*'):
            return [k for k in permutation_set if k.startswith(token[:len(token) - 1])]
        else:
            portions = token.split('*')
            for index, portion in enumerate(portions):
                if index == 0:
                    permutation_set = [
                        k for k in permutation_set if k.startswith(portion)]
                elif index == len(portions) - 1:
                    permutation_set = [
                        k for k in permutation_set if k.endswith(portion)]
                else:
                    permutation_set = [
                        k for k in permutation_set if portion in k]
            return permutation_set


# Optional Module: Wildcard Management
def build_bigram_index(inv_index, token):
    """
        Build out the bigram index and return it
        Structure is as follows:

        {
            "se": ["sentence","license",...],
            ...
        }
        A dict with string as key, and the values are a list of strings with bigram included
    """
    bigrams = [token[i:i + 2] for i in range(1, len(
        token) - 1, 2)]  # Get all bigrams from the 2nd letter to the 2nd-last letter
    bigrams.append(token[0])  # first letter
    bigrams.append(token[-1])  # last letter
    bigrams = [''.join(b for b in bigram if b not in '*')  # Filter out any * in the bigrams, as that was causing problems earlier during inverted index search
               for bigram in bigrams]
    return {bigram: [index for index in inv_index.keys() if bigram in index] for bigram in bigrams}
