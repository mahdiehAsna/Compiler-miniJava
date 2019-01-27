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
    def __init__(self, symbolTable):
        super().__init__()
        self.currentClass = ""
        self.currentMethodType = ""
        self.lastExpressionType = ""
        self.codeStore = {}
        self.code = ""
        self.isInitialized = False

        self.symbolTable = symbolTable

        self.block_number = 0
        self.variables = {}


    def get_bytecode(self):
        return self.codeStore

    @staticmethod
    def get_representation(s_type):
        if s_type == 'int':
            return 'I'
        if s_type == 'boolean':
            return 'Z'

    @staticmethod
    def get_return_by_type(s_type):
        #todo implement array
        if s_type == 'int':
            return 'ireturn'
        if s_type == 'boolean':
            return 'ireturn'

    def enterMainClass(self, ctx:MinijavaParser.MainClassContext):
        self.currentClass = ctx.getChild(1).getText()
        self.code += '.class public %s' % self.currentClass + '\n'
        self.code += '.super java/lang/Object' + '\n'
        self.code += '.method public <init>()V' + '\n'
        self.code += 'aload_0' + '\n'
        self.code += 'invokenonvirtual java/lang/Object/<init>()V' + '\n'
        self.code += 'return' + '\n'
        self.code += '.end method' + '\n'
        self.code += '.method public static main([Ljava/lang/String;)V' + '\n'
        self.code += '.limit stack 10000' + '\n'

    def exitMainClass(self, ctx: MinijavaParser.MainClassContext):
        self.code += "return" + '\n'
        self.code += ".end method" + '\n'
        self.codeStore[self.currentClass] = self.code
        self.code = ""

    def enterClassDeclaration(self, ctx:MinijavaParser.ClassDeclarationContext):
        print("enterClassDeclaration")
        self.isInitialized = False
        self.currentClass = ctx.getChild(1).getText()
        self.code += '.class public %s' % self.currentClass + '\n'
        self.code += '.super java/lang/Object' + '\n'

    def exitClassDeclaration(self, ctx:MinijavaParser.ClassDeclarationContext):
        self.codeStore[self.currentClass] = self.code
        self.code = ""

    #todo other filed types
    def enterFieldDeclaration(self, ctx:MinijavaParser.FieldDeclarationContext):
        field_name = ctx.getChild(0).getChild(1).getText()
        field_properties = self.symbolTable[self.currentClass][field_name]
        field_type = field_properties['return_type']
        field_type_representation = self.get_representation(field_type)
        if field_type == 'int':
            self.code += '.field private %s %s' % (field_name, field_type_representation) + '\n'

    def enterMethodDeclaration(self, ctx:MinijavaParser.MethodDeclarationContext):
        if not self.isInitialized:
            self.code += '.method public <init>()V' + '\n'
            self.code += 'aload_0' + '\n'
            self.code += 'invokenonvirtual java/lang/Object/<init>()V' + '\n'
            self.code += 'return' + '\n'
            self.code += '.end method' + '\n'
        self.currentMethodType = ctx.getChild(1).getText()
        method_name = ctx.getChild(2).getText()

        self.code += '.method public %s' % method_name

        if ctx.getChild(4).getText() == ')':
            return_type_representation = self.get_representation(self.currentMethodType)
            self.code += '()%s' % return_type_representation + '\n'

    def exitMethodDeclaration(self, ctx: MinijavaParser.MethodDeclarationContext):
        self.code += '.end method' + '\n'

    def enterParameterList(self, ctx:MinijavaParser.ParameterListContext):
        self.code += '('

    def exitParameterList(self, ctx: MinijavaParser.ParameterListContext):
        return_type_representation = self.get_representation(self.currentMethodType)
        self.code += ')%s' % return_type_representation + '\n'

    def enterMethodBody(self, ctx:MinijavaParser.MethodBodyContext):
        self.code += '.limit stack 10000' + '\n'
        #todo implement .limit locals
        self.code += ''

    def exitMethodBody(self, ctx:MinijavaParser.MethodBodyContext):
        self.code += self.get_return_by_type(self.currentMethodType) + '\n'

    def enterObjectInstantiationExpression(self, ctx:MinijavaParser.ObjectInstantiationExpressionContext):
        object_class_name = ctx.getChild(1).getText()
        self.code += 'new %s' % object_class_name + '\n'
        self.code += 'dup' + '\n'
        self.code += 'invokespecial %s/<init>()V' % object_class_name + '\n'

    def exitObjectInstantiationExpression(self, ctx:MinijavaParser.ObjectInstantiationExpressionContext):
        object_class_name = ctx.getChild(1).getText()
        self.lastExpressionType = object_class_name

    def exitMethodCallExpression(self, ctx: MinijavaParser.MethodCallExpressionContext):
        #todo implement method inputs
        method_name = ctx.getChild(2).getText()
        print("gi")
        print(self.lastExpressionType)
        print(method_name)
        class_properties = self.symbolTable[self.lastExpressionType][method_name]
        return_type_representation = self.get_representation(class_properties["return_type"])
        self.code += 'invokevirtual %s/%s(%s)%s' % (self.lastExpressionType, method_name, '', return_type_representation) + '\n'

    def enterLocalDeclaration(self, ctx:MinijavaParser.LocalDeclarationContext):
        #todo
        var_name = ctx.getChild(1).getText()
        var_properties= self.symbolTable[self.currentClass][var_name]
        if var_properties['return_type'] == 'int':
            self.code += 'bipush 0' + '\n'
            self.code += 'istore' + '\n'

    def enterVariableAssignmentStatement(self, ctx:MinijavaParser.VariableAssignmentStatementContext):
        name = ctx.getChild(0).getText()
        properties = self.symbolTable[self.currentClass][name]
        type = properties['type']
        if type == 'field':
            self.code += 'aload 0 ; push this' + '\n'

    #todo var type
    def exitVariableAssignmentStatement(self, ctx:MinijavaParser.VariableAssignmentStatementContext):
        name = ctx.getChild(0).getText()
        properties = self.symbolTable[self.currentClass][name]
        type = properties['type']
        if type == 'field':
            return_type = properties['return_type']
            representation = self.get_representation(return_type)
            self.code += 'putfield %s/%s %s' % (self.currentClass, name, representation) + '\n'

    def exitPowExpression(self, ctx:MinijavaParser.PowExpressionContext):
        #todo implement
        print()
        print("exitPowExpression")
        self.code += "" + '\n'

    def exitMulExpression(self, ctx:MinijavaParser.MulExpressionContext):
        print()
        print("exitMulExpression")
        self.code += "imul" + '\n'

    def exitBasicMathExpression(self, ctx:MinijavaParser.BasicMathExpressionContext):
        print("exitBasicMathExpression")
        type = ctx.getChild(1).getText()
        if type == '+':
            self.code += "iadd" + '\n'
        elif type == '-':
            self.code += "isub" + '\n'

    def enterIntLitExpression(self, ctx:MinijavaParser.IntLitExpressionContext):
        literal = ctx.getChild(0).getText()
        print("enterIntLitExpression %s" % literal)
        self.code += "ldc %s" % literal + '\n'

    def enterIdentifierExpression(self, ctx:MinijavaParser.IdentifierExpressionContext):
        name = ctx.getChild(0).getText()
        properties = self.symbolTable[self.currentClass][name]
        type = properties['type']
        if type == 'field':
            return_type = properties['return_type']
            representation = self.get_representation(return_type)
            self.code += 'aload 0 ; push this' + '\n'
            self.code += 'getfield %s/%s %s' % (self.currentClass, name, representation) + '\n'

    def enterPrintStatement(self, ctx: MinijavaParser.PrintStatementContext):
        self.code += "getstatic java/lang/System/out Ljava/io/PrintStream;" + '\n'

    def exitPrintStatement(self, ctx:MinijavaParser.PrintStatementContext):
        self.code += "invokevirtual java/io/PrintStream/println(I)V" + '\n'


    def enterLtExpression(self, ctx:MinijavaParser.LtExpressionContext):
        print()
        print("enterLtExpression")
        self.code += ""

    def enterAndExpression(self, ctx:MinijavaParser.AndExpressionContext):
        print()
        print("enterAndExpression")
        self.code += ""
