#!/usr/bin/python

from env import Env
import maltypes, printer, reader

repl_env = Env(None)
repl_env.set(maltypes.Symbol("+"), lambda x, y: x + y)
repl_env.set(maltypes.Symbol("-"), lambda x, y: x - y)
repl_env.set(maltypes.Symbol("*"), lambda x, y: x * y)
repl_env.set(maltypes.Symbol("/"), lambda x, y: int(x / y))

def READ(line):
    return reader.read_str(line)

def EVAL(mt, env):
    if type(mt) == list:
        if mt[0] == "def!":
            val = EVAL(mt[2], env)
            env.set(mt[1], val)
            return val

        elif mt[0] == "let*":
            new_env = Env(env)
            bindings = mt[1]
            for i in range(0, len(bindings), 2):
                val = EVAL(bindings[i+1], new_env)
                new_env.set(bindings[i], val)
            return EVAL(mt[2], new_env)

        else:
            l = eval_ast(mt, env)
            f = l[0]
            return f(*l[1:])

    else:
        return eval_ast(mt, env)

def PRINT(mt):
    return printer.pr_str(mt)

def eval_ast(ast, env):
    if type(ast) == maltypes.Symbol:
        return env.get(ast)
    elif type(ast) == list:
        return [EVAL(e, env) for e in ast]
    else:
        return ast

def rep(line):
    return PRINT(EVAL(READ(line), repl_env))

def main():
    while True:
        try:
            line = raw_input("user> ")
            print rep(line)
        except EOFError, eofe:
            print
            break

if __name__ == "__main__":
    main()
