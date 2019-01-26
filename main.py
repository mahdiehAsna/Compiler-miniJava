import sys
from antlr4 import *
from grammer.MinijavaLexer import MinijavaLexer
from grammer.MinijavaParser import MinijavaParser
from MinijavaPrintListener import MiniJavaPrintListener


def main(argv):

    file_addr = argv[1]
    file_name = file_addr.split('/')[-1]
    name = file_name.split('.')[0]

    file = open(file_addr)
    text = file.read()

    input = InputStream(text)
    lexer = MinijavaLexer(input)
    stream = CommonTokenStream(lexer)

    parser = MinijavaParser(stream)
    tree = parser.goal()

    printer = MiniJavaPrintListener(name)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    bytecode = printer.get_bytecode()

    output = open('intermediateCode/' + name + '.j', 'w')

    output.write(bytecode)


if __name__ == '__main__':
    main(sys.argv)