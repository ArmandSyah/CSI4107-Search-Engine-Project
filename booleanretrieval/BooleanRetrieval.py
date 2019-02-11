import json


class BooleanRetrieval():
    def __init__(self, inv_index):
        with open('corpus.json') as corpus:
            c = json.load(corpus)
            self.complete_set = {document['doc_id'] for document in c}
        self.inverted_index = inv_index
        self.boolean_tokens = ["AND", "OR", "NOT"]

    def retrieve(self, query):
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
        if token in self.inverted_index:
            appearances = self.inverted_index[token]
            return {appearance.doc_id for appearance in appearances}
        return set()

    def check_permutations(self, token):
        if token.startswith('*'):
            return [k for k in self.inverted_index.keys() if k.endswith(token[1:])]
        elif token.endswith('*'):
            return [k for k in self.inverted_index.keys() if k.startswith(token[:len(token) - 1])]
