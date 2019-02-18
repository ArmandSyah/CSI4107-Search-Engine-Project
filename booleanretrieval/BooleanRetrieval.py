import json
from utilities import *


class BooleanRetrieval():
    def __init__(self, inv_index):
        with open('corpus.json') as corpus:
            c = json.load(corpus)
            self.complete_set = {document['doc_id'] for document in c}
        self.inverted_index = inv_index
        self.boolean_tokens = ["AND", "OR", "NOT"]
        self.mode = 'unaltered'

    def retrieve(self, query, mode):
        query = lowercase_folding(query)
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
        token_list = query.split()

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
                    print(permutations)
                    querystack.append(self.postfix_retrieval(
                        ' OR '.join(permutations)))
                else:
                    querystack.append(self.perform_retrieve(token))

        for operation in opstack:
            if operation == 'AND':
                if len(querystack) >= 2:
                    queries, querystack = querystack[:2], querystack[2:]
                    operand1, operand2 = queries[0], queries[1]
                    intersect_between = operand1.intersection(operand2)
                    querystack.insert(0, intersect_between)
            elif operation == 'OR':
                if len(querystack) >= 2:
                    queries, querystack = querystack[:2], querystack[2:]
                    operand1, operand2 = queries[0], queries[1]
                    union_between = operand1.union(operand2)
                    querystack.insert(0, union_between)
            elif operation == 'NOT':
                if len(querystack) >= 1:
                    query, querystack = querystack[:1], querystack[1:]
                    difference_between = self.complete_set - query
                    querystack.insert(0, difference_between)

        return querystack.pop()

    def perform_retrieve(self, token):
        if token in self.inverted_index[self.mode]:
            appearances = self.inverted_index[self.mode][token]
            return {appearance.doc_id for appearance in appearances}
        return set()

    def check_permutations(self, token):
        bigram_index = build_bigram_index(
            self.inverted_index[self.mode], token)
        permutation_set = set()
        for _, ind_list in bigram_index.items():
            if len(permutation_set) == 0:
                permutation_set.update(ind_list)
            else:
                permutation_set.intersection(ind_list)

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


def build_bigram_index(inv_index, token):
    bigrams = [token[i:i + 2] for i in range(1, len(token) - 1, 2)]
    bigrams.append(token[0])  # first letter
    bigrams.append(token[-1])  # last letter
    bigrams = [''.join(b for b in bigram if b not in '*')
               for bigram in bigrams]
    return {bigram: [index for index in inv_index.keys() if bigram in index] for bigram in bigrams}
