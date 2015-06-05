#!/usr/bin/python

import printer, reader

repl_env = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: int(x / y)
}

def READ(line):
    return reader.read_str(line)

def EVAL(dt, env):
    if type(dt) == list:
        l = eval_ast(dt, env)
        return l[0](*l[1:])
    else:
        return eval_ast(dt, env)

def PRINT(dt):
    return printer.pr_str(dt)

def eval_ast(ast, env):
    if type(ast) == str:
        if ast in env:
            return env[ast]
        else:
            raise Exception("'%s' not found" % ast)
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
