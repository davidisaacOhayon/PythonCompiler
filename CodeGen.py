import Parser as Parser
import Lexer as lex
import SemanticAnalysis as sem
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
                              
                    fun test(x:bool) -> int{
                        if (x == true){
                              return 5;
                        }
                    }
                              
                    """)
    parserObj.Parse()

    sAnalyzer = sem.SemanticAnalyzer(parserObj.ASTroot)
    sAnalyzer.analyze()
    print_visitor = ast.PrintNodesVisitor()
    parserObj.ASTroot.accept(print_visitor)

