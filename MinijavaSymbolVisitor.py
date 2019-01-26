from grammer.MinijavaVisitor import MinijavaVisitor
from grammer.MinijavaParser import MinijavaParser

class MinijavaSymbolVisitor(MinijavaVisitor):
    def __init__(self):
        super().__init__()
        self.currentClass = ""
        self.symbolTable = {}

    def get_symbol_table(self):
        return self.symbolTable

    def visitClassDeclaration(self, ctx:MinijavaParser.ClassDeclarationContext):
        self.currentClass = ctx.getChild(1).getText()
        self.symbolTable[self.currentClass] = {}

        return self.visitChildren(ctx)

    def visitMethodDeclaration(self, ctx:MinijavaParser.MethodDeclarationContext):
        method_type = ctx.getChild(1).getText()
        method_name = ctx.getChild(2).getText()
        self.symbolTable[self.currentClass][method_name] = {"type": method_type, "inputes": []}

        return self.visitChildren(ctx)

    def visitParameter(self, ctx: MinijavaParser.ParameterContext):
        #todo implement input param

        return self.visitChildren(ctx)
