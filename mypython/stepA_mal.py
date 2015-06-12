#!/usr/bin/python

import sys
import traceback

import core
from env import Env
import maltypes, printer, reader

repl_env = Env(None)

def call(f, ast, env):
    if f.ast is not None:
        ast = f.ast
        new_env = Env(f.env, f.params, l[1:])
        env = new_env
    return ast

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

def is_macro_call(ast, env):
    return (type(ast) == list and type(ast[0]) == maltypes.Symbol and
            env.find(ast[0]) is not None and env.get(ast[0]).is_macro == True)

def macroexpand(ast, env):
    while is_macro_call(ast, env) == True:
        macro = env.get(ast[0])
        if macro.fn is None:
            raise Exception("Not a user-defined function")
        ast = macro.fn(*ast[1:])
    return ast

def READ(line):
    return reader.read_str(line)

def EVAL(ast, env):
    while True:
        if type(ast) == list:
            # Apply

            ast = macroexpand(ast, env)
            if type(ast) != list:
                return ast

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
                def func(*params):
                    new_env = Env(env, ast[1], params)
                    res = EVAL(ast[2], new_env)
                    return res;
                return maltypes.Function(ast[2], ast[1], env, func)

            elif ast[0] == "quote":
                return ast[1]

            elif ast[0] == "quasiquote":
                ast = quasiquote(ast[1])
                continue

            elif ast[0] == "defmacro!":
                val = EVAL(ast[2], env)
                if type(val) != maltypes.Function:
                    raise Exception("Not a function")
                val.is_macro = True
                env.set(ast[1], val)
                return val

            elif ast[0] == "macroexpand":
                return macroexpand(ast[1], env)

            elif ast[0] == "try*":
                if ast[2][0] == "catch*":
                    try:
                        return EVAL(ast[1], env)
                    except Exception, e:
                        value = e.args[0]
                        if type(e) == maltypes.MalException:
                            value = e.value
                        ex_env = Env(env, [ast[2][1]], [value])
                        return EVAL(ast[2][2], ex_env)
                else:
                    return EVAL(ast[1], env)

            else:
                # Apply
                l = eval_ast(ast, env)
                f = l[0]
                if type(f) == maltypes.Function:
                    if f.ast is not None:
                        ast = f.ast
                        new_env = Env(f.env, f.params, l[1:])
                        env = new_env
                        continue
                    else:
                        return f.fn(*l[1:])
                else:
                    raise Exception("Not a mal function")

        else:
            return eval_ast(ast, env)

def PRINT(ast):
    res = printer.pr_str(ast, print_readably=True)
    return res

def eval_ast(ast, env):
    if type(ast) == list:
        return [EVAL(e, env) for e in ast]
    elif type(ast) == dict:
        items = []
        for k in ast.keys():
            items.append(EVAL(k, env))
            items.append(EVAL(ast[k], env))
        return core.make_dict(*items)
    elif type(ast) == maltypes.Vector:
        return maltypes.Vector([EVAL(e, env) for e in ast])
    elif type(ast) == maltypes.Symbol:
        return env.get(ast)
    else:
        return ast

def rep(line):
    return PRINT(EVAL(READ(line), repl_env))

def main():
    for sym, func in core.ns.iteritems():
        repl_env.set(sym, maltypes.Function(None, None, None, func, name=sym.name))

    repl_env.set(maltypes.Symbol("eval"),
                 maltypes.Function(None, None, None,
                                   lambda ast: EVAL(ast, repl_env),
                                   name="eval"));

    rep('(def! *host-language* "Python")')
    rep('(def! not (fn* (a) (if a false true)))')
    rep('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) ")")))))')
    rep("(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))")
    rep("(defmacro! or (fn* (& xs) (if (empty? xs) nil (if (= 1 (count xs)) (first xs) `(let* (or_FIXME ~(first xs)) (if or_FIXME or_FIXME (or ~@(rest xs))))))))")

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
