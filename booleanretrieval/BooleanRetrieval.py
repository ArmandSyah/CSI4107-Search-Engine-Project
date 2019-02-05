import json


class BooleanRetrieval():
    def __init__(self, inv_index):
        with open('corpus.json') as corpus:
            c = json.load(corpus)
            self.complete_set = [document['doc_id'] for document in c]
        self.inverted_index = inv_index
        self.boolean_tokens = ["AND", "OR", "NOT"]

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
        token_list = postfix_query.split()
        current_set = self.complete_set

        for token in token_list:
            if token in self.boolean_tokens:
                op2 = opstack.pop()
                op1 = opstack.pop()
                current_set = retrieve(token, op1, op2, current_set)
                opstack.append(result)
            else:
                opstack.append(token)

        return current_set

    def retrieval(self, token, op1, op2, current_set):
