import json


class BooleanRetrieval():
    def __init__(self):
        with open('corpus.json') as corpus:
            self.corpus = json.load(corpus)

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
