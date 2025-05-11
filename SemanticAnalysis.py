
import Parser as Parser
import Lexer as lex
import ASTNodes as ast




# typetable = {lex.TokenType.BooleanLiteral : lex.TokenType.BoolType, lex.TokenType.}



class SemanticAnalyzer:
    def __init__(self, root):
        self.symbol_table = {}
        self.index = 0
        self.root = root

        
    # Used for error checking function blocks only
    def analyze_block(self, node):
        tempIndex = 0
        innerSymbolTable = {}
        returnType = node.returnType
        hasReturn = False
        while (tempIndex < len(node.block.stmts)):
            currentNode = node.block.stmts[tempIndex]

            match type(currentNode):
                case ast.ASTAssignmentNode:
                    if currentNode.id.lexeme in innerSymbolTable.keys():
                        raise Exception(f"Variable {currentNode.id.lexeme} already Declared in function {node.name}")
                    innerSymbolTable[currentNode.id.lexeme]  = { "type" : "assign", "varType" : currentNode.expr.type }
                    tempIndex += 1
                    continue
                
                case ast.ASTDeclareNode:
                    if currentNode.id in innerSymbolTable :
                        innerSymbolTable[currentNode.var] = {"type" : "declare", "varType" : currentNode.type }
                        tempIndex += 1
                        continue
                
                case ast.ASTFunctionNode:
                    raise Exception(f"Cannot define nested functions, in {node.name}.")
                

                case ast.ASTReturnNode:
                    if currentNode.type != returnType:
                        raise SyntaxError(f"return type in {node.name} does not match defined return type of function. Expected {returnType}, got {currentNode.type}")
                    hasReturn = True
                    tempIndex += 1

                case ast.ASTFunctionCall:
                    if currentNode.name in self.symbol_table.keys():
                        temp_index += 1
                        continue
                    else:
                        raise Exception(f"Function {currentNode.name} is not defined.")
 
                case _:
                    raise SyntaxError("Invalid Statement")
        
        if not hasReturn:
            raise Exception(f"Funciton {node.name} returns no value.")


    def analyze(self):
        # Get root block
        Block = self.root.block
        # Iterate throughout block statements   
        while (self.index < len(Block.stmts)):
            # Get current node
            currentNode = Block.stmts[self.index]

            # Match case of nodes
            match type(currentNode):
                # Assignment node
                case ast.ASTAssignmentNode:
                    if currentNode.id.lexeme in self.symbol_table.keys():
                        raise Exception(f"Variable {currentNode.id.lexeme} already declared. ")
                    self.symbol_table[currentNode.id.lexeme]  = { "type" : "assign", "varType" : currentNode.expr.type }
                    self.index += 1
                    continue

                case ast.ASTReAssignNode:
                    if currentNode.id.lexeme in self.symbol_table.keys():
                        self.symbol_table[currentNode.id.lexeme]  = { "type" : "reassign", "varType" : currentNode.expr.type }
                        self.index += 1
                        continue
                    else:
                        raise Exception(f"Variable {currentNode.id.lexeme} isn't defined.")
                # Declare node ()
                case ast.ASTDeclareNode:
                    self.symbol_table[currentNode.var] = {"type" : "declare", "varType" : currentNode.type }
                    self.index += 1
                    continue
                
                case ast.ASTFunctionNode:
                    if currentNode.name not in self.symbol_table.keys():
                            self.symbol_table[currentNode.name] = {"func_name" : currentNode.name, "type" : "function", "returnType" : currentNode.returnType }
                            self.analyze_block(currentNode)
                            self.index += 1
                            continue
                    raise Exception("Function already declared.")


                case ast.ASTFunctionCall:
                    if currentNode.name in self.symbol_table.keys():
                        self.index += 1
                        continue
                    else:
                        raise Exception(f"Function {currentNode.name} is not defined.")

                case ast.ASTIfNode:
                    self.index += 1
                    continue

                case ast.ASTWhileNode:
                    self.index += 1
                    continue

                case ast.ASTForNode:
                    self.index += 1
                    continue
 
                case _:
                    raise SyntaxError("Invalid Statement")

           

    def displaySymbolTable(self):
        print(self.symbol_table)

            

        




if "__main__" == __name__:

    input = '''
                int x = 5;  
            '''
    
    parserObj = Parser.Parser("""
                    while ((p1 < p2) and (p2 < 3)){
                        let x:int = 2;          
                    }
                              
                    test()
                    """)
    parserObj.Parse()

    print_visitor = ast.PrintNodesVisitor()
    parserObj.ASTroot.accept(print_visitor)
    sAnalyzer = SemanticAnalyzer(parserObj.ASTroot)
    sAnalyzer.analyze()
    sAnalyzer.displaySymbolTable()
