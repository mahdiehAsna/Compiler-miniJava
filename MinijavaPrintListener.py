from grammer.MinijavaListener import MinijavaListener
from grammer.MinijavaParser import MinijavaParser


def keyboard(banner=None):
    import code, sys

    # use exception trick to pick up the current frame
    try:
        raise None
    except:
        frame = sys.exc_info()[2].tb_frame.f_back

    # evaluate commands in current namespace
    namespace = frame.f_globals.copy()
    namespace.update(frame.f_locals)

    code.interact(banner=banner, local=namespace)

class MiniJavaPrintListener(MinijavaListener):
    def __init__(self, name):
        super().__init__()
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
        print()
        print("enterAddExpression")
        self.code += "iadd" + '\n'

    def exitMulExpression(self, ctx:MinijavaParser.MulExpressionContext):
        print()
        print("enterMulExpression")
        self.code += "imul" + '\n'

    def exitSubExpression(self, ctx:MinijavaParser.SubExpressionContext):
        print()
        print("enterSubExpression")
        self.code += "isub" + '\n'

    def exitIntLitExpression(self, ctx:MinijavaParser.IntLitExpressionContext):
        print()

        literal = ctx.getChild(0).getText()
        print("enterIntLitExpression %s" % literal)
        self.code += "ldc %s" % literal + '\n'

    
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


    def enterPrintStatement(self, ctx: MinijavaParser.PrintStatementContext):
        self.code += "getstatic java/lang/System/out Ljava/io/PrintStream;" + '\n'

    def exitPrintStatement(self, ctx:MinijavaParser.PrintStatementContext):
        self.code += "invokevirtual java/io/PrintStream/println(I)V" + '\n'
