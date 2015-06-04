import re

MATCH = """[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)"""

class Reader:
    def __init__(self, tokens):
        self.pos_ = 0
        self.tokens_ = tokens

    def peek(self):
        if self.pos_ >= len(self.tokens_):
            return ""
        return self.tokens_[self.pos_]

    def next(self):
        token = self.peek()
        if token != "":
            self.pos_ = self.pos_ + 1
        return token

def read_str(string):
    tokens = tokenizer(string)
    r = Reader(tokens)
    return read_form(r)

def tokenizer(string):
    regex = re.compile(MATCH)
    tokens = [token for token in regex.findall(string) if len(token) > 0]
    # print tokens
    return tokens

def read_form(reader):
    token = reader.peek()
    c = token[0]
    if c == "(":
        res = read_list(reader)
    else:
        res = read_atom(reader)
    return res

def read_list(reader):
    res = []
    reader.next() # consume (
    while reader.peek()[0] != ")":
        res.append(read_form(reader))
    reader.next() # consume )
    return res

def read_atom(reader):
    atom = reader.next()
    try:
        res = int(atom)
    except:
        res = atom
    return res
