import maltypes

ns = {}

ns[maltypes.Symbol("+")] = lambda x, y: x + y
ns[maltypes.Symbol("-")] = lambda x, y: x - Y
ns[maltypes.Symbol("*")] = lambda x, y: x * y
ns[maltypes.Symbol("/")] = lambda x, y: int(x / y)

def count(*x):
    if x[0] == None:
        return 0
    else:
        return len(x[0])

ns[maltypes.Symbol("list")] = lambda *x: list(x)
ns[maltypes.Symbol("list?")] = lambda *x: type(x[0]) == list
ns[maltypes.Symbol("empty?")] = lambda *x: len(x[0]) == 0
ns[maltypes.Symbol("count")] = count

def equals(e, other):
    if type(e) != type(other):
        return False
    if type(e) == maltypes.Symbol:
        return e.name == other.name
    elif type(e) == list:
        return (len(e) == len(other)
                and all([equals(e[i], other[i]) for i in range(len(e))]))
    else:
        return e == other

ns[maltypes.Symbol("=")] = equals

ns[maltypes.Symbol("<")] = lambda x, y: x < y
ns[maltypes.Symbol("<=")] = lambda x, y: x <= y
ns[maltypes.Symbol(">")] = lambda x, y: x > y
ns[maltypes.Symbol(">=")] = lambda x, y: x >= y
