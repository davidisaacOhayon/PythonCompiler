
import Parser as Parser
import Lexer as lex
import ASTNodes as ast






class SemanticAnalyzer:
    def __init__(self, root):
        self.symbol_table = {}
        self.index = 0
        self.root = root

    def add_symbol(self, symbol, value):
        self.symbol_table[symbol] = value


    def analyze(self):
        






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
