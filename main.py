import sys
from antlr4 import *
from grammer.MinijavaLexer import MinijavaLexer
from grammer.MinijavaParser import MinijavaParser
from MinijavaPrintListener import MiniJavaPrintListener
from MinijavaErrorListener import MinijavaErrorListener
from MinijavaSymbolVisitor import MinijavaSymbolVisitor


def main(argv):

    file_addr = argv[1]
    file_name = file_addr.split('/')[-1]
    name = file_name.split('.')[0]

    file = open(file_addr)
    text = file.read()

    input = InputStream(text)
    lexer = MinijavaLexer(input)
    lexer.addErrorListener(MinijavaErrorListener())

    stream = CommonTokenStream(lexer)

    parser = MinijavaParser(stream)
    tree = parser.goal()

    visitor = MinijavaSymbolVisitor()
    visitor.visitGoal(tree)

    symbol_table = visitor.get_symbol_table()
    print(symbol_table)

    printer = MiniJavaPrintListener(symbol_table)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    codeStore = printer.get_bytecode()

    for className, classCode in codeStore.items():
        output = open('intermediateCode/' + className + '.j', 'w')
        output.write(classCode)


if __name__ == '__main__':
    main(sys.argv)