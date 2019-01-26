from grammer import MinijavaListener, MinijavaParser


class MiniJavaPrintListener(MinijavaListener):
    def __init__(self, name):
        super(MinijavaListener, self).__init__()
        self.code = ""
        self.name = name
        self.block_number = 0
        self.variables = {}

    def get_bytecode(self):
        return self.code

    def enterGoal(self, ctx: MinijavaParser.GoalContext):
        self.code += '.class public %s' % self.name + '\n'
        self.code += '.super java/lang/Object' + '\n'
        self.code += '.method public <init>()V' + '\n'
        self.code += 'aload_0' + '\n'
        self.code += 'invokenonvirtual java/lang/Object/<init>()V' + '\n'
        self.code += 'return' + '\n'
        self.code += '.end method' + '\n'
        self.code += '.method public static main([Ljava/lang/String;)V' + '\n'
        self.code += '.limit stack 10000' + '\n'

    def exitGoal(self, ctx:MinijavaParser.GoalContext):
        self.code += "return" + '\n'
        self.code += ".end method" + '\n'

    def exitAddExpression(self, ctx:MinijavaParser.AddExpressionContext):
        self.code += "iadd" + '\n'
        print()
        print("enterAddExpression")

    def exitMulExpression(self, ctx:MinijavaParser.MulExpressionContext):
        print()
        print("enterMulExpression")
        self.code += "imul"

    def exitSubExpression(self, ctx:MinijavaParser.SubExpressionContext):
        print()
        print("enterSubExpression")
    self.code += "isub"

    
    def enterVarDeclaration(self, ctx:MinijavaParser.VarDeclarationContext):
        print()

    def enterLtExpression(self, ctx:MinijavaParser.LtExpressionContext):
        print()
        print("enterLtExpression")
        self.code += ""

    def enterAndExpression(self, ctx:MinijavaParser.AndExpressionContext):
        print()
        print("enterAndExpression")
        self.code += ""
        
    def enterPowExpression(self, ctx:MinijavaParser.PowExpressionContext):
        print()
        print("enterPowExpression")
        self.code += ""

