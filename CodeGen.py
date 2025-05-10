import Parser as Parser
import Lexer as lex
import ASTNodes as ast



class Frame:
    def __init__(self, name):
        self.name = name
        self.scope = []



class CodeGen:
    def __init__(self):
        self.opStack = []
        self.addressStack = {}
        self.instructions = []
        self.pIndex = 0
        self.memory = []
        self.program = [".main"]

    def mainExec(self):
        pass


    def oFrame(self):
        pass

    def visitFunction(self, node):
        funcName = node.name
        self.addressStack[node.name] = self.pIndex
        self.program.append(f".{funcName}")

        

    
    def push(self, arg):
        if int(arg):
            self.opStack.append(arg)
        






    




if "__main__" == __name__:

    input = '''
                int x = 5;  
            '''
    
    parserObj = Parser.Parser("""
                    test(5, true);
                    
                    """)
    parserObj.Parse()

    print_visitor = ast.PrintNodesVisitor()
    parserObj.ASTroot.accept(print_visitor)

