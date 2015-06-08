#!/usr/bin/python

import sys
import traceback

import core
from env import Env
import maltypes, printer, reader

repl_env = Env(None)

def is_pair(ast):
    return type(ast) == list and len(ast) > 0

def quasiquote(ast):
    if not is_pair(ast):
        return [maltypes.Symbol("quote"), ast]
    elif ast[0] == "unquote":
        return ast[1]
    elif is_pair(ast[0]) and ast[0][0] == "splice-unquote":
        return [maltypes.Symbol("concat"), ast[0][1], quasiquote(ast[1:])]
    else:
        return [maltypes.Symbol("cons"), quasiquote(ast[0]), quasiquote(ast[1:])]

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
                # elements = eval_ast(ast[1:], env)
                # return elements[-1]
                eval_ast(ast[1:-1], env)
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

            elif ast[0] == "quote":
                return ast[1]

            elif ast[0] == "quasiquote":
                ast = quasiquote(ast[1])
                continue

            else:
                l = eval_ast(ast, env)
                f = l[0]
                if type(f) == maltypes.Function:
                    ast = f.ast
                    new_env = Env(f.env, f.params, l[1:])
                    env = new_env
                    continue
                else:
                    return f(*l[1:])

        else:
            return eval_ast(ast, env)

def PRINT(ast):
    res = printer.pr_str(ast, print_readably=True)
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
    for sym, d in core.ns.iteritems():
        repl_env.set(sym, d)

    repl_env.set("eval", lambda ast: EVAL(ast, repl_env))

    rep('(def! not (fn* (a) (if a false true)))')
    rep('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) ")")))))')

    repl_env.set("*ARGV*", sys.argv[2:])
    if len(sys.argv) > 1:
        rep('(load-file "%s")' % sys.argv[1])
        sys.exit(0)

    while True:
        try:
            line = raw_input("user> ")
            print rep(line)
        except Exception, e:
            print traceback.format_exc(limit=10)
            continue
        except EOFError, eofe:
            print
            break

if __name__ == "__main__":
    main()
