#!/usr/bin/python

def READ(line):
	return line

def EVAL(line):
	return line

def PRINT(line):
	return line

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
