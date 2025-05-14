

import Parser as Parser
import Lexer as lex
import SemanticAnalysis as sem
import ASTNodes as ast

class CodeGen:
    def __init__(self, program):
        # Instructions array holding final product
        self.instructions = ['.main']

        # Symbol Table
        self.symbolTable = {}
        # Index
        self.index = 0
        # Code
        self.root = program

    
    def emit(self, ins):
        self.instructions.append(ins)
        self.index += 1


    def evaluate(self):
        # Loop through code
        Block = self.root.block

        while self.index < len(Block):
            currentNode = Block[self.index]



        

    def oFrame(self):
        self.emit('oframe')

    def cFrmae(self):
        self.emit('cframe')



if __name__ == "__main__":
    parserObj = Parser.Parser("""
                    let x:int = 5;
                              

                    """)
    parserObj.Parse()

    print_visitor = ast.PrintNodesVisitor()
    parserObj.ASTroot.accept(print_visitor)
    sAnalyzer = SemanticAnalyzer(parserObj.ASTroot)
    sAnalyzer.analyze()

