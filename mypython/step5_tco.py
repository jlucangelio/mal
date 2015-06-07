#!/usr/bin/python

import core
from env import Env
import maltypes, printer, reader

repl_env = Env(None)
for sym, d in core.ns.iteritems():
    repl_env.set(sym, d)

def READ(line):
    return reader.read_str(line)

def EVAL(ast, env):
    while True:
        if type(ast) == list:
            if ast[0] == "def!":
                val = EVAL(ast[2], env)
                env.set(ast[1], val)
                return val

            elif ast[0] == "let*":
                new_env = Env(env)
                bindings = ast[1]
                for i in range(0, len(bindings), 2):
                    val = EVAL(bindings[i+1], new_env)
                    new_env.set(bindings[i], val)
                # return EVAL(ast[2], new_env)
                ast = ast[2]
                env = new_env
                continue

            elif ast[0] == "do":
                # elements = [eval_ast(e, env) for e in ast[1:]]
                # return elements[-1]
                [eval_ast(e, env) for e in ast[1:-1]]
                ast = ast[-1]
                continue

            elif ast[0] == "if":
                cond = EVAL(ast[1], env)
                if cond != None and cond != False:
                    # cond was true
                    ast = ast[2]
                else:
                    if len(ast) > 3:
                        ast = ast[3]
                    else:
                        return None
                continue

            elif ast[0] == "fn*":
                # def func(*params):
                #     new_env = Env(env, ast[1], params)
                #     res = EVAL(ast[2], new_env)
                #     return res;
                return maltypes.Function(ast[2], ast[1], env)

            else:
                l = eval_ast(ast, env)
                f = l[0]
                if type(f) == maltypes.Function:
                    ast = f.ast
                    new_env = Env(f.env, f.params, l[1:])
                    env = new_env
                else:
                    return f(*l[1:])

        else:
            res = eval_ast(ast, env)
            return res

def PRINT(ast):
    res = printer.pr_str(ast)
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
