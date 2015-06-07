#!/usr/bin/python

import core
from env import Env
import maltypes, printer, reader

repl_env = Env(None)
for sym, d in core.ns.iteritems():
    repl_env.set(sym, d)

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

        elif mt[0] == "do":
            elements = [eval_ast(e, env) for e in mt[1:]]
            return elements[-1]

        elif mt[0] == "if":
            cond = EVAL(mt[1], env)
            if cond != None and cond != False:
                # cond was true
                res = EVAL(mt[2], env)
            else:
                if len(mt) > 3:
                    res = EVAL(mt[3], env)
                else:
                    res = maltypes.Nil()
            return res

        elif mt[0] == "fn*":
            def func(*params):
                new_env = Env(env, mt[1], params)
                res = EVAL(mt[2], new_env)
                return res;
            return func

        else:
            l = eval_ast(mt, env)
            func = l[0]
            return func(*l[1:])

    else:
        res = eval_ast(mt, env)
        return res

def PRINT(mt):
    res = printer.pr_str(mt)
    return res

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
