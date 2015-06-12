import maltypes
import printer, reader
import copy

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

def seq_equals(e, other):
    seqs = [list, maltypes.Vector]
    return (type(e) in seqs and type(other) in seqs
            and len(e) == len(other)
            and all([equals(e[i], other[i]) for i in range(len(e))]))

def equals(e, other):
    if type(e) == list:
        return seq_equals(e, other)
    elif type(e) == maltypes.Vector:
        return seq_equals(e, other)
    elif type(e) != type(other):
        return False
    if type(e) == maltypes.Symbol:
        return e.name == other.name
    elif type(e) == list:
        return seq_equals(e, other)
    elif type(e) == maltypes.Vector:
        return seq_equals(e, other)
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
    s = " ".join([printer.pr_str(arg, False) for arg in args])
    print s
    return None

ns[maltypes.Symbol("prn")] = prn
ns[maltypes.Symbol("println")] = println

ns[maltypes.Symbol("read-string")] = reader.read_str

def slurp(filename):
    with open(filename) as f:
        return f.read()

ns[maltypes.Symbol("slurp")] = slurp

ns[maltypes.Symbol("cons")] = lambda x, xs: [x] + list(xs)

def concat(*ls):
    res = []
    [res.extend(l) for l in ls]
    return res

ns[maltypes.Symbol("concat")] = concat

def first(l):
    if len(l) > 0:
        return l[0]
    return None

ns[maltypes.Symbol("nth")] = lambda l, n: l[n]
ns[maltypes.Symbol("first")] = first
ns[maltypes.Symbol("rest")] = lambda l: l[1:]

def throw(value):
     raise maltypes.MalException(value)

ns[maltypes.Symbol("throw")] = throw

def apply(f, *xs):
    if vector_q(xs[-1]):
        l = xs[-1].l
    else:
        l = xs[-1]
    return f.fn(*(list(xs[0:-1]) + l))

ns[maltypes.Symbol("apply")] = apply

def map(f, xs):
    if vector_q(xs):
        l = xs.l
    else:
        l = xs
    return [f.fn(e) for e in l]

ns[maltypes.Symbol("map")] = map

ns[maltypes.Symbol("nil?")] = lambda arg: arg is None
ns[maltypes.Symbol("true?")] = lambda arg: arg == True
ns[maltypes.Symbol("false?")] = lambda arg: arg == False

ns[maltypes.Symbol("symbol")] = lambda arg: maltypes.Symbol(arg)
ns[maltypes.Symbol("symbol?")] = lambda arg: type(arg) == maltypes.Symbol

ns[maltypes.Symbol("keyword")] = lambda arg: maltypes.Keyword.fromstring(arg)
ns[maltypes.Symbol("keyword?")] = lambda arg: type(arg) == maltypes.Keyword

ns[maltypes.Symbol("vector")] = lambda *xs: maltypes.Vector(xs)

def vector_q(arg):
    return type(arg) == maltypes.Vector

ns[maltypes.Symbol("vector?")] = vector_q

ns[maltypes.Symbol("sequential?")] = lambda arg: (type(arg) == list
                                                  or type(arg) == maltypes.Vector)

def make_dict(*args):
    return dict([(args[i], args[i+1]) for i in range(0, len(args), 2)])

ns[maltypes.Symbol("hash-map")] = make_dict
ns[maltypes.Symbol("map?")] = lambda arg: type(arg) == dict

def assoc(m, *xs):
    mprime = copy.copy(m)
    # TODO: Figure why this is needed.
    if type(mprime) ==  tuple:
        m = m[0]
        mprime = mprime[0]
    mprime.update(make_dict(*xs))
    return mprime

ns[maltypes.Symbol("assoc")] = assoc

def dissoc(m, *keys):
    res = copy.copy(m)
    for k in keys:
        if k in res:
            del res[k]
    return res

ns[maltypes.Symbol("dissoc")] = dissoc

def get(m, k):
    if m is None:
        return None
    else:
        return m.get(k, None)

ns[maltypes.Symbol("get")] = get
ns[maltypes.Symbol("contains?")] = lambda m, k: k in m
ns[maltypes.Symbol("keys")] = lambda m: list(m.keys())
ns[maltypes.Symbol("vals")] = lambda m: list(m.values())

ns[maltypes.Symbol("readline")] = raw_input

ns[maltypes.Symbol("atom")] = lambda v: maltypes.Atom(v)
ns[maltypes.Symbol("atom?")] = lambda a: type(a) == maltypes.Atom
ns[maltypes.Symbol("deref")] = lambda a: a.value

def reset(a, v):
    a.value = v
    return a.value

ns[maltypes.Symbol("reset!")] = reset

def swap(a, f, *args):
    a.value = f.fn(a.value, *args)
    return a.value

ns[maltypes.Symbol("swap!")] = swap

ns[maltypes.Symbol("meta")] = lambda f: f.metadata

def withmeta(f, m):
    fprime = copy.copy(f)
    fprime.metadata = m
    return fprime

ns[maltypes.Symbol("with-meta")] = withmeta
