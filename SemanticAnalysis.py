
import Parser as Parser
import Lexer as lex
import ASTNodes as ast



# Note: token types were separated (e.g. Integer & Integertype) to prevent
# identifiers such as int from being parsed as actual Integer nodes with a value holder.
# So, we're relying on this type exchange.
# Identifiers have to be evaluated in code gen.
types = {lex.TokenType.Integer : lex.TokenType.IntegerType,
         lex.TokenType.FloatLiteral : lex.TokenType.FloatType,
         lex.TokenType.BooleanLiteral : lex.TokenType.BoolType}

class SemanticAnalyzer:
    def __init__(self, root):
        # Symbol table
        self.symbol_table = {}
        # Current index
        self.index = 0
        # Current frame level 
        self.level = 0
        # Root node
        self.root = root
        # Used for functions to temporarily track and validate returns
        self.current_ret_type = None

    # Used to analyze basic blocks, typically within if, for or while statements
    def analyze_block(self, node):
        # Increment level
        self.level += 1
        # Indexing for block statements
        tempIndex = 0
        # Symbol table for checks
        innerSymbolTable = {}
        # check if block has return
        hasReturn = False
        # Variable counter
        varCount = 0

        while (tempIndex < len(node.block.stmts)):
            # Get current node statement
            currentNode = node.block.stmts[tempIndex]

            match type(currentNode):

                case ast.ASTAssignmentNode:
                    if currentNode.id.lexeme in innerSymbolTable.keys():
                        raise Exception(f"Variable {currentNode.id.lexeme} already Declared in function {node.name}")
                    innerSymbolTable[currentNode.id.lexeme]  = { "type" : "assign", "varType" : currentNode.expr.type, "index": self.index + tempIndex, "level" : self.level }
                    tempIndex += 1
                    varCount += 1
                    continue

                case ast.ASTReAssignNode:
                    if currentNode.id.lexeme in self.symbol_table.keys() or currentNode.id.lexeme in innerSymbolTable.keys():
                        tempIndex += 1
                        continue
                    else:
                        raise Exception(f"Variable {currentNode.id.lexeme} isn't defined.")
                
                case ast.ASTDeclareNode:
                    if currentNode.id in innerSymbolTable :
                        innerSymbolTable[currentNode.var] = {"type" : "declare", "varType" : currentNode.type,  "index":  self.index + tempIndex , "level" : self.level }
                        tempIndex += 1
                        varCount += 1
                        continue
                
                case ast.ASTFunctionNode:
                    raise Exception(f"Cannot define nested functions, in {node.name}.")
                

                case ast.ASTReturnNode:
                    # Check if we have a function return type (this always knows if we're inside a function or not)
                    if currentNode.type == lex.TokenType.Identifier:
                        # Evaluate expression later
                        pass
                    elif self.current_ret_type != None:
                        if types[currentNode.type] != self.current_ret_type:
                            raise SyntaxError("Return Type does not match function return type")
                    tempIndex += 1
                    hasReturn = True
                    continue

                case ast.ASTFunctionCall:
                    if currentNode.name in self.symbol_table.keys():
                        tempIndex += 1
                        continue
                    else:
                        raise Exception(f"Function {currentNode.name} is not defined.")
                    
                case ast.ASTIfNode:
                    # Checks block and also finds return

                    
                    result = self.analyze_block(currentNode)
                    tempIndex += 1
                    varCount += 1
                    
                    if result:
                        hasReturn = True
                
                    continue

                case ast.ASTWhileNode:
                    
                     
                    result = self.analyze_block(currentNode)
                    tempIndex += 1
                    varCount += 1
                    if result:
                        hasReturn = True
                  
                    continue

                case ast.ASTPrintNode:
                    self.index += 1
                    continue

                case ast.ASTForNode:
                    # Checks block and also finds return
                   
                    # Get for loop init variable
                    if currentNode.init.id in self.symbol_table.keys():
                        raise Exception(f"Variable {currentNode.id.lexeme} already declared. ")
                    # add to symbol table
                    self.symbol_table[currentNode.init.id.lexeme]  = { "type" : "assign", "varType" : currentNode.init.expr.type, "index" :  self.index + tempIndex, "level" : self.level}
                    varCount +=1
                    tempIndex += 1
                
                     
                    result = self.analyze_block(currentNode)
                    
                    varCount += 1
                    if result:
                        hasReturn = True
                 
                    continue
 
                case _:
                    raise SyntaxError("Invalid Statement")
            
        self.symbol_table.update(innerSymbolTable)
        self.level -= 1
        return varCount, hasReturn
        

    # Used for error checking function blocks only

    def analyze_formal_params(self, node):
        # Iterate through each formal parameter
        for x in node.params:
            self.symbol_table[x.var] = {"type" : x.type, "index": self.index, "level": self.level}
            self.index += 1
            
    def analyze_func_block(self, node):
        # Increment level
        self.level += 1
        # Temporary index within function
        tempIndex = 0
        # Inner symbol for checking
        innerSymbolTable = {}
        # Return type
        returnType = node.returnType
        # If func has return (for syntax check)
        hasReturn = False
        # Variable counter
        varCount = 0
        while (tempIndex < len(node.block.stmts)):
            currentNode = node.block.stmts[tempIndex]

            match type(currentNode):
                case ast.ASTAssignmentNode:
                    if currentNode.id.lexeme in innerSymbolTable.keys():
                        raise Exception(f"Variable {currentNode.id.lexeme} already Declared in function {node.name}")
                    innerSymbolTable[currentNode.id.lexeme]  = { "type" : "assign", "varType" : currentNode.expr.type, "index":  self.index + tempIndex, "level" : self.level }
                    tempIndex += 1
                    varCount += 1
 
                    continue
                case ast.ASTReAssignNode:
                    if currentNode.id.lexeme in self.symbol_table.keys() or currentNode.id.lexeme in innerSymbolTable.keys():
                        tempIndex += 1
                        continue
                    else:
                        raise Exception(f"Variable {currentNode.id.lexeme} isn't defined.")
                
                case ast.ASTDeclareNode:
                    if currentNode.id in innerSymbolTable :
                        innerSymbolTable[currentNode.var] = {"type" : "declare", "varType" : currentNode.type, "index":  self.index + tempIndex, "level" : self.level }
                        tempIndex += 1
                        varCount +=1 
                        continue
                
                case ast.ASTFunctionNode:
                    raise Exception(f"Cannot define nested functions, in {node.name}.")
                

                case ast.ASTReturnNode:
                    # If we are returning an identifier
                    if currentNode.type == lex.TokenType.Identifier:
                        # Identifier has to be evaluated later on
                        pass
                    elif types[currentNode.type] != returnType:
                        raise SyntaxError(f"return type in {node.name} does not match defined return type of function. Expected {returnType}, got {currentNode.type}")
                    hasReturn = True
                    tempIndex += 1

                case ast.ASTFunctionCall:
                    if currentNode.name in self.symbol_table.keys():
                        tempIndex += 1
                        continue
                    else:
                        raise Exception(f"Function {currentNode.name} is not defined.")
                    
                case ast.ASTIfNode:
                    # Checks block and also finds return
             
                    result = self.analyze_block(currentNode)
               
                    if result:
                        hasReturn = True

                    tempIndex += 1
                    continue

                case ast.ASTWhileNode:
                    # Checks block and also finds return
                 
                    result = self.analyze_block(currentNode)
               
                    if result:
                        hasReturn = True
                    tempIndex += 1
                    continue

                case ast.ASTForNode:
                    # Checks block and also finds return
                    tempIndex += 1
                    # Get for loop init variable
                    if currentNode.init.id.lexeme in self.symbol_table.keys():
                        raise Exception(f"Variable {currentNode.id.lexeme} already declared. ")
                    # add to symbol table
                    self.symbol_table[currentNode.init.id]  = { "type" : "assign", "varType" : currentNode.init.expr.type, "index" :  self.index + tempIndex, "level" : self.level}
                    varCount +=1
                    tempIndex += 1
                    # Get for loop condition
              
                    result = self.analyze_block(currentNode)
                     
                    if result:
                        hasReturn = True
                    tempIndex += 1
                    continue
 
                case _:
                    raise SyntaxError("Invalid Statement")
 
        self.symbol_table.update(innerSymbolTable)
        self.level -= 1
        if not hasReturn:
            raise Exception(f"Funciton {node.name} returns no value.")


    # def analyze_params(self, params):


    def analyze(self):
        
        # Get root block
        Block = self.root.block
        varCount = 0
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
                    self.symbol_table[currentNode.id.lexeme]  = { "type" : "assign", "varType" : currentNode.expr.type, "index" : self.index, "level" : self.level}
                    self.index += 1
                    continue

                case ast.ASTReAssignNode:
                    if currentNode.id.lexeme in self.symbol_table.keys():
                        self.index += 1
                        continue
                    else:
                        raise Exception(f"Variable {currentNode.id.lexeme} isn't defined.")
                # Declare node ()
                case ast.ASTDeclareNode:
                    self.symbol_table[currentNode.var] = {"type" : "declare", "varType" : currentNode.type, "index": self.index, "level" : self.level  }
                    self.index += 1
                    continue
                
                case ast.ASTFunctionNode:
                    if currentNode.name not in self.symbol_table.keys():
                            # self.symbol_table[currentNode.name] = {"func_name" : currentNode.name, "type" : "function", "returnType" : currentNode.returnType, "param_types" : [x.type for x in currentNode.params.params if x != None], "index": self.index, "level" : self.level }
                            self.analyze_formal_params(currentNode.params)
                            self.index += 1
                            self.current_ret_type = currentNode.returnType
                            self.analyze_func_block(currentNode)
                            self.current_ret_type = None

                            continue
                    raise Exception("Function already declared.")

                case ast.ASTPrintNode:
                    self.index += 1
                    continue

                case ast.ASTFunctionCall:
                    # Check if function is defined
                    if currentNode.name in self.symbol_table.keys():
                        # Get function
                        function = self.symbol_table[currentNode.name]
                        # check if paramters match
                        if not len(currentNode.params.params) == len(function["param_types"]):
                            raise SyntaxError(f"Parameters of function call {currentNode.name} does not match definition.")
                        
                        # match parameter types
                        for i, param in enumerate(currentNode.params.params):
                            # Parameter locations should match
                            if types[param.type] != function["param_types"][i]:
                                raise SyntaxError(f"Parameter types of call {currentNode.name} do not match function definition.")
                        self.index += 1

                        continue
                    else:
                        raise Exception(f"Function {currentNode.name} is not defined.")
                    

                case ast.ASTIfNode:
                
                    self.analyze_block(currentNode)
                    self.index += 1
                  
                    continue

                case ast.ASTWhileNode:
                    
                    self.analyze_block(currentNode)
                    self.index += 1
                   
                    continue

                case ast.ASTPrintNode:
                    self.index += 1
                    continue

                case ast.ASTForNode:
                    # Get for loop init variable
                    if currentNode.init.id.lexeme in self.symbol_table.keys():
                        raise Exception(f"Variable {currentNode.id.lexeme} already declared. ")
                    # add to symbol table
                    self.symbol_table[currentNode.init.id.lexeme]  = { "type" : "assign", "varType" : currentNode.init.expr.type, "index" : self.index, "level" : self.level}
                    varCount +=1
                    self.index += 1

                    self.analyze_block(currentNode)

  
                     
                    continue
 
                case _:
                    raise SyntaxError("Invalid Statement")

           

    def displaySymbolTable(self):
            print(self.symbol_table)

            

        




if "__main__" == __name__:

 
    
    parserObj = Parser.Parser("""
                    fun test(x:int, y:bool) -> int {
                        a:int = 5;
                        return a;       
                    }

                    """)
    parserObj.Parse()

    print_visitor = ast.PrintNodesVisitor()
    parserObj.ASTroot.accept(print_visitor)
    sAnalyzer = SemanticAnalyzer(parserObj.ASTroot)
    sAnalyzer.analyze()
    sAnalyzer.displaySymbolTable()
