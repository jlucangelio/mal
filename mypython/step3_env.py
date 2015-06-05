#!/usr/bin/python

from env import Env
import printer, reader

repl_env = Env(None)
repl_env.set("+", lambda x, y: x + y)
repl_env.set("-", lambda x, y: x - y)
repl_env.set("*", lambda x, y: x * y)
repl_env.set("/", lambda x, y: int(x / y))

def READ(line):
    return reader.read_str(line)

def EVAL(dt, env):
    if type(dt) == list:
        if dt[0] == "def!":
            val = EVAL(dt[2], env)
            env.set(dt[1], val)
            return val

        elif dt[0] == "let*":
            new_env = Env(env)
            bindings = dt[1]
            for i in range(0, len(bindings), 2):
                val = EVAL(bindings[i+1], new_env)
                new_env.set(bindings[i], val)
            return EVAL(dt[2], new_env)

        else:
            l = eval_ast(dt, env)
            f = l[0]
            return f(*l[1:])

    else:
        return eval_ast(dt, env)

def PRINT(dt):
    return printer.pr_str(dt)

def eval_ast(ast, env):
    if type(ast) == str:
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
