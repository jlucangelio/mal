import maltypes
import printer, reader

ns = {}

ns[maltypes.Symbol("+")] = lambda x, y: x + y
ns[maltypes.Symbol("-")] = lambda x, y: x - y
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

ns[maltypes.Symbol("pr-str")] = lambda *args: " ".join(
        [printer.pr_str(arg, True) for arg in args])

ns[maltypes.Symbol("str")] = lambda *args: "".join(
        [printer.pr_str(arg, False) for arg in args])

def prn(*args):
    s = " ".join([printer.pr_str(arg, True) for arg in args])
    print s
    return None

def println(*args):
    s = "".join([printer.pr_str(arg, False) for arg in args])
    print s
    return None

ns[maltypes.Symbol("prn")] = prn
ns[maltypes.Symbol("println")] = println

ns[maltypes.Symbol("read-string")] = reader.read_str

def slurp(filename):
    with open(filename) as f:
        return f.read()

ns[maltypes.Symbol("slurp")] = slurp

ns[maltypes.Symbol("cons")] = lambda x, xs: [x] + xs

def concat(*ls):
    res = []
    [res.extend(l) for l in ls]
    return res

ns[maltypes.Symbol("concat")] = concat
