class Type(object):
    def __init__(self):
        pass

    def __str__(self):
        raise Exception("Not implemented")

class Symbol(Type):
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        return self.name == other

    def __str__(self):
        return self.name

class Keyword(Symbol):
    @classmethod
    def fromstring(cls, string):
        return cls(":" + string)

    def __init__(self, name):
        self.name = name

class Atom(Symbol):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "(atom %s)" % self.value

class Function(Type):
    def __init__(self, ast, params, env, fn=None, is_macro=False, metadata=None,
                       name="#<function>"):
        self.ast = ast
        self.params = params
        self.env = env
        self.fn = fn
        self.is_macro = is_macro
        self.metadata = metadata
        self.name = name

    def __str__(self):
        return "#<%s>" % self.name

class Vector(Type):
    def __init__(self, elems):
        self.l = list(elems)

    def __str__(self):
        return "[" + " ".join([str(e) for e in self.l]) + "]"

    def __len__(self):
        return len(self.l)

    def __getitem__(self, i):
        return self.l[i]

class MalException(Exception):
    def __init__(self, value):
        super(Exception, self).__init__("MalException")
        self.value = value

# class Nil(Type):
#     def __init__(self):
#         pass

#     def __str__(self):
#         return "nil"

# class Boolean(Type):
#     def __init__(self):
#         pass

# class True(Boolean):
#     def __init__(self):
#         pass

#     def __str__(self):
#         return "true"

# class False(Boolean):
#     def __init__(self):
#         pass

#     def __str__(self):
#         return "false"
