#!/usr/bin/python

import printer, reader

def READ(line):
    return reader.read_str(line)

def EVAL(dt):
    return dt

def PRINT(dt):
    return printer.pr_str(dt)

def rep(line):
    return PRINT(EVAL(READ(line)))

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
