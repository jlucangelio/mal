import re

import maltypes

MATCH = """[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)"""

class Reader:
    def __init__(self, tokens):
        self.pos_ = 0
        self.tokens_ = tokens

    def peek(self):
        if self.pos_ >= len(self.tokens_):
            return None
        return self.tokens_[self.pos_]

    def next(self):
        token = self.peek()
        if token != None:
            self.pos_ = self.pos_ + 1
        return token

def read_str(string):
    tokens = tokenizer(string)
    r = Reader(tokens)
    return read_form(r)

def tokenizer(string):
    regex = re.compile(MATCH)
    tokens = [token for token in regex.findall(string) if len(token) > 0]
    return tokens

def read_form(reader):
    token = reader.peek()
    c = token[0]
    if c == "(":
        res = read_list(reader)
    elif c == "[":
        res = read_vector(reader)
    else:
        res = read_atom(reader)
    return res

def read_list(reader):
    return read_seq(reader, "(", ")")

def read_vector(reader):
    return read_seq(reader, "[", "]")

def read_seq(reader, b, e):
    res = []
    reader.next() # consume b
    while reader.peek()[0] != e:
        res.append(read_form(reader))
    reader.next() # consume e
    return res

def read_atom(reader):
    token = reader.next()
    res = None
    try:
        res = int(token)
    except:
        # It's not a number.
        if token == "nil":
            res = None
        elif token == "true":
            res = True
        elif token == "false":
            res = False
        elif token[0] == '"':
            res = token[1:-1].replace(r'\"', '"')
        else:
            res = maltypes.Symbol(token)
    return res
