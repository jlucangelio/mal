class Env:
    def __init__(self, outer, binds=[], exprs=[]):
        self.outer = outer
        self.data = {}
        for i, s in enumerate(binds):
            self.set(s, exprs[i])

    def set(self, symbol, value):
        self.data[symbol] = value

    def find(self, symbol):
        if symbol in self.data:
            return self
        elif self.outer is not None:
            return self.outer.find(symbol)
        else:
            return None

    def get(self, symbol):
        env = self.find(symbol)
        if env is not None:
            return env.data[symbol]
        else:
            raise Exception("'%s' not found" % symbol)
