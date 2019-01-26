import sys
from antlr4 import *
from grammer.MinijavaLexer import MinijavaLexer
from grammer.MinijavaParser import MinijavaParser
from MinijavaPrintListener import MiniJavaPrintListener


def main(argv):
    file = open('sample/math.minijava')
    text = file.read()

    input = InputStream(text)
    lexer = MinijavaLexer(input)
    stream = CommonTokenStream(lexer)

    parser = MinijavaParser(stream)
    tree = parser.goal()

    printer = MiniJavaPrintListener('math')
    walker = ParseTreeWalker()
    walker.walk(printer, tree)


if __name__ == '__main__':
    main(sys.argv)