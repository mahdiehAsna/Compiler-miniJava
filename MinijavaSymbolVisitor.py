from grammer.MinijavaVisitor import MinijavaVisitor
from grammer.MinijavaParser import MinijavaParser

class MinijavaSymbolVisitor(MinijavaVisitor):
    def __init__(self):
        super().__init__()
        self.currentClass = ""
        self.currentMethod = ""
        self.symbolTable = {}
        self.variables = {}

    def get_symbol_table(self):
        return self.symbolTable

    def new_variable(self, name):
        new_id = len(self.variables[self.currentClass]) + 1
        self.variables[self.currentClass][name] = new_id
        return new_id

    def visitClassDeclaration(self, ctx:MinijavaParser.ClassDeclarationContext):
        self.currentClass = ctx.getChild(1).getText()
        self.symbolTable[self.currentClass] = {}
        self.variables[self.currentClass] = {}

        return self.visitChildren(ctx)

    def visitFieldDeclaration(self, ctx:MinijavaParser.FieldDeclarationContext):
        field_type = ctx.getChild(0).getChild(0).getText()
        field_name = ctx.getChild(0).getChild(1).getText()
        field_id = self.new_variable(field_name)
        self.symbolTable[self.currentClass][field_name] = {"type": "field", "return_type": field_type, "id": field_id}

    def visitVarDeclaration(self, ctx: MinijavaParser.VarDeclarationContext):
        var_type = ctx.getChild(0).getText()
        var_name = ctx.getChild(1).getText()
        var_id = self.new_variable(var_name)
        self.symbolTable[self.currentClass][var_name] = {"type": "var", "return_type": var_type, "id": var_id}

        return self.visitChildren(ctx)

    def visitMethodDeclaration(self, ctx:MinijavaParser.MethodDeclarationContext):
        method_type = ctx.getChild(1).getText()
        method_name = ctx.getChild(2).getText()
        self.currentMethod = method_name
        self.symbolTable[self.currentClass][method_name] = {"type": "method", "return_type": method_type, "inputs": []}

        return self.visitChildren(ctx)

    def visitParameterList(self, ctx:MinijavaParser.ParameterListContext):
        for child in ctx.getChildren():
            if child.getText() != ',':
                param_type = child.getChild(0).getText()
                param_name = child.getChild(1).getText()
                param_prop = (param_type, param_name)
                print(param_prop, "ZZZZZZ")
                self.symbolTable[self.currentClass][self.currentMethod]["inputs"].append(param_prop)
                var_type = param_type
                var_name = param_name
                var_id = self.new_variable(var_name)
                self.symbolTable[self.currentClass][var_name] = {"type": "var", "return_type": var_type, "id": var_id}

    # todo implement input param
    def visitParameter(self, ctx: MinijavaParser.ParameterContext):
        return self.visitChildren(ctx)

