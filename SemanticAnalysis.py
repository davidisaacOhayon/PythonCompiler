
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
        self.symbol_table = {"functions" : {}}
        # Index ( used for symbol table allocation)
        self.index = 0
        # Position index
        self.pos = 0
        # Current frame level 
        self.level = 0
        # Root node
        self.root = root
        # Used for functions to temporarily track and validate returns
        self.current_ret_type = None

    # Used to analyze basic blocks, typically within if, for or while statements
    # Index variable is also used incases of statements within functions
    # Symbol table of functions is passed too
    def analyze_block(self, node, symbolTable=None):
        # Increment level
        self.level += 1
        # temporary index
        tempIndex = 0 
        # position indexfor block statements
        tempPos = 0
        # Symbol table for checks
        innerSymbolTable = {}
        # check if block has return
        hasReturn = False
        # Variable counter
        varCount = 0

        while (tempPos < len(node.block.stmts)):
            # Get current node statement
            currentNode = node.block.stmts[tempPos]

            match type(currentNode):

                case ast.ASTAssignmentNode:
                    tempIndex += 1
                    if currentNode.id.lexeme in innerSymbolTable.keys():
                        raise Exception(f"Variable {currentNode.id.lexeme} already Declared in function {node.name}")
                    innerSymbolTable[currentNode.id.lexeme]  = { "type" : "assign", "varType" : currentNode.expr.type, "index": tempIndex, "level" : self.level }
                    tempPos += 1
                    varCount += 1
                    continue

                case ast.ASTReAssignNode:
                    if currentNode.id.lexeme in self.symbol_table.keys() or currentNode.id.lexeme in innerSymbolTable.keys():
                        tempPos += 1
                        continue
                    else:
                        raise Exception(f"Variable {currentNode.id.lexeme} isn't defined.")
                
                case ast.ASTDeclareNode:
                    if currentNode.id in innerSymbolTable :
                        innerSymbolTable[currentNode.var] = {"type" : "declare", "varType" : currentNode.type,  "index":  tempIndex, "level" : self.level }
                        tempPos += 1
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
                    tempPos += 1
                    hasReturn = True
                    continue

                case ast.ASTFunctionCall:
                    if currentNode.name in self.symbol_table.keys():
                        tempPos += 1
                        continue
                    else:
                        raise Exception(f"Function {currentNode.name} is not defined.")
                    
                case ast.ASTIfNode:
                    # Checks block and also finds return

                    result = self.analyze_block(currentNode, tempIndex)
                    tempPos += 1
                    varCount += 1
                    
                    if result:
                        hasReturn = True
                
                    continue

                case ast.ASTWhileNode:
                    
                     
                    result = self.analyze_block(currentNode, tempIndex)
                    tempPos += 1
                    varCount += 1
                    if result:
                        hasReturn = True
                  
                    continue

                case ast.ASTPrintNode:
                    tempPos += 1
                    continue

                case ast.ASTWriteBoxNode:
                    tempPos += 1
                    continue

                case ast.ASTForNode:
                    # Checks block and also finds return
                    tempIndex +=1
                    # Get for loop init variable
                    if currentNode.init.id in self.symbol_table.keys():
                        raise Exception(f"Variable {currentNode.id.lexeme} already declared. ")
                    # add to symbol table
                    self.symbol_table[currentNode.init.id.lexeme]  = { "type" : "assign", "varType" : currentNode.init.expr.type, "index" :  tempIndex, "level" : self.level}
                    varCount +=1
                    tempPos += 1
                
                     
                    result = self.analyze_block(currentNode, tempIndex)
                    
                    varCount += 1
                    if result:
                        hasReturn = True
                 
                    continue
 
                case _:
                    raise SyntaxError("Invalid Statement")
        if symbolTable != None:
            symbolTable.update(innerSymbolTable)
        else :
            self.symbol_table.update(innerSymbolTable)
        self.level -= 1
        return varCount, hasReturn
        

    # Used for error checking function blocks only

    def analyze_formal_params(self, node):
        # temporary symbol table
        tempSymbolTable = {}
        # temp position for tracking function location
        tempPos = 0
        # Check if function node has params 
        if len(node.params) > 0:
            # Iterate through each formal parameter
            for x in node.params:
                if x == None:
                    continue
                # add to symbol table
                tempSymbolTable[x.var] = {"type" : x.type, "index": tempPos, "level": self.level}
                # increment temp position
                tempPos += 1

        # return symbol table and position to function
        return tempSymbolTable, tempPos
            
    def analyze_func_block(self, node):
        # The index variable is to keep track of positions for the inner symbol table
        tempIndex = 0 
        # Temporary position within function
        tempPos = 0
        # Inner symbol for checking
        innerSymbolTable = {}
        # Return type
        returnType = node.returnType
        # If func has return (for syntax check)
        hasReturn = False
        # Variable counter
        varCount = 0
        while (tempPos < len(node.block.stmts)):
            currentNode = node.block.stmts[tempPos]
            # Increment temp index
            tempIndex += 1
            match type(currentNode):
                case ast.ASTAssignmentNode:
                    # Check if variable is already declared
                    if currentNode.id.lexeme in innerSymbolTable.keys():
                        # Raise error
                        raise Exception(f"Variable {currentNode.id.lexeme} already Declared in function {node.name}")
                    # Assign variable to inner symbol table
                    innerSymbolTable[currentNode.id.lexeme]  = { "type" : "assign", "varType" : currentNode.expr.type, "index": tempIndex, "level" : self.level }

                    # Increment temp position
                    tempPos += 1
                    # increase var count
                    varCount += 1
 
                    continue
                case ast.ASTReAssignNode:
                    # Check if variable is declared
                    if currentNode.id.lexeme in self.symbol_table.keys() or currentNode.id.lexeme in innerSymbolTable.keys():
                        # Increment temp positon
                        tempPos += 1
                        continue
                    else:
                        # Raise error
                        raise Exception(f"Variable {currentNode.id.lexeme} isn't defined.")              
                case ast.ASTDeclareNode:
                    # Check if variable is already declared
                    if currentNode.id in innerSymbolTable:
                        innerSymbolTable[currentNode.var] = {"type" : "declare", "varType" : currentNode.type, "index": tempIndex, "level" : self.level }
                        # increment temp position
                        tempPos += 1
                        # increment var count
                        varCount +=1 
                        continue
                case ast.ASTFunctionNode:
                    raise Exception(f"Cannot define nested functions, in {node.name}.")
                

                case ast.ASTReturnNode:
                    # If we are returning an identifier
                    if currentNode.type == lex.TokenType.Identifier:
                        # Identifier has to be evaluated later on
                        pass
                    # If return type does not match function return type
                    elif types[currentNode.type] != returnType:
                        # raise error
                        raise SyntaxError(f"return type in {node.name} does not match defined return type of function. Expected {returnType}, got {currentNode.type}")
                    hasReturn = True
                    tempPos += 1

                case ast.ASTFunctionCall:
                    # check if function is declared
                    if currentNode.name in self.symbol_table.keys():
                        # increment position
                        tempPos += 1
                        continue
                    else:
                        # raise error
                        raise Exception(f"Function {currentNode.name} is not defined.")
                    
                case ast.ASTIfNode:
                    # Checks block and also finds return
                
                    result = self.analyze_block(currentNode, innerSymbolTable)
               
                    if result:
                        hasReturn = True

                    tempPos += 1
                    continue

                case ast.ASTWhileNode:
                    # Checks block and also finds return
                 
                    result = self.analyze_block(currentNode, innerSymbolTable)
               
                    if result:
                        hasReturn = True
                    tempPos += 1
                    continue
                
                case ast.ASTPrintNode:
                    tempPos += 1
                    continue
                case ast.ASTForNode:
                    # Checks block and also finds return
                    tempPos += 1
                    # Get for loop init variable
                    if currentNode.init.id.lexeme in self.symbol_table.keys():
                        raise Exception(f"Variable {currentNode.id.lexeme} already declared. ")
                    # add to symbol table
                    self.symbol_table[currentNode.init.id.lexeme]  = { "type" : "assign", "varType" : currentNode.init.expr.type, "index" :  tempIndex, "level" : self.level}
                    varCount +=1
                    tempPos += 1
                    # Get for loop condition
              
                    result = self.analyze_block(currentNode, innerSymbolTable)
                     
                    if result:
                        hasReturn = True
                    tempPos += 1
                    continue
 
                case _:
                    raise SyntaxError("Invalid Statement")
 
        self.symbol_table.update(innerSymbolTable)
 
        if not hasReturn:
            raise Exception(f"Funciton {node.name} returns no value.")


    # def analyze_params(self, params):
    def analyze(self):
        
        # Get root block
        Block = self.root.block
        varCount = 0
        # Iterate throughout block statements   
        while (self.pos < len(Block.stmts)):
            # Get current node
            currentNode = Block.stmts[self.pos]

            # Match case of nodes
            match type(currentNode):
                # Assignment node
                case ast.ASTAssignmentNode:
                    if currentNode.id.lexeme in self.symbol_table.keys():
                        raise Exception(f"Variable {currentNode.id.lexeme} already declared. ")
                    # Assign to symbol table 
                    self.symbol_table[currentNode.id.lexeme]  = { "type" : "assign", "varType" : currentNode.expr.type, "index" : self.index, "level" : self.level}
                    # Increment symbol table index
                    self.index +=1
                    # Increment statement block position
                    self.pos += 1
                    continue

                case ast.ASTReAssignNode:
                    if currentNode.id.lexeme in self.symbol_table.keys():
                        continue
                    else:
                        raise Exception(f"Variable {currentNode.id.lexeme} isn't defined.")
                # Declare node ()
                case ast.ASTDeclareNode:
                    self.symbol_table[currentNode.var] = {"type" : "declare", "varType" : currentNode.type, "index": self.index, "level" : self.level  }
                    self.pos += 1
                    continue
                
                case ast.ASTFunctionNode:
                    if currentNode.name not in self.symbol_table.keys():
                            # Define function onto the symbol table
                            self.symbol_table["functions"][currentNode.name] = {"func_name" : currentNode.name, "symbolTable" : {}}
                            self.symbol_table["functions"][currentNode.name]['param_types'] = [x.type for x in currentNode.params.params]
                            # process formal parameters, and check function frame index
                            self.symbol_table["functions"][currentNode.name]["symbolTable"], funcIndex = self.analyze_formal_params(currentNode.params)
                            self.pos += 1
                            # Get function return type
                            self.current_ret_type = currentNode.returnType
                            # analyze function block
                            self.analyze_func_block(currentNode)
                            # set current return type to none
                            self.current_ret_type = None

                            continue
                    
                    raise Exception("Function already declared.")

                case ast.ASTPrintNode:
                    self.pos += 1
                    continue

                case ast.ASTFunctionCall:
                    print(self.symbol_table['functions'])
                    # Check if function is defined
                    if currentNode.name in self.symbol_table['functions'].keys():
                        # Get function
                        function = self.symbol_table['functions'][currentNode.name]
                        # check if paramters match
                        if not len(currentNode.params.params) == len(function["param_types"]):
                            raise SyntaxError(f"Parameters of function call {currentNode.name} does not match definition.")
                        
                        # match parameter types
                        # for i, param in enumerate(currentNode.params.params):
                        #     # Parameter locations should match
                        #     if types[param.type] != function["param_types"][i]:
                        #         raise SyntaxError(f"Parameter types of call {currentNode.name} do not match function definition.")
                        self.pos += 1

                        continue
                    else:
                        raise Exception(f"Function {currentNode.name} is not defined.")
                    

                case ast.ASTIfNode:
                
                    self.analyze_block(currentNode)
                    self.pos += 1
                  
                    continue

                case ast.ASTWhileNode:
                    
                    self.analyze_block(currentNode)
                    self.pos += 1
                   
                    continue

                case ast.ASTPrintNode:
                    self.pos += 1
                    continue

                case ast.ASTWriteBoxNode:
                    self.pos += 1
                    continue

                case ast.ASTForNode:
                    # Get for loop init variable
                    if currentNode.init.id.lexeme in self.symbol_table.keys():
                        raise Exception(f"Variable {currentNode.id.lexeme} already declared. ")
                    # add to symbol table
                    self.symbol_table[currentNode.init.id.lexeme]  = { "type" : "assign", "varType" : currentNode.init.expr.type, "index" : self.index, "level" : self.level}
                    varCount +=1
                    self.pos += 1

                    self.analyze_block(currentNode)

  
                     
                    continue
 
                case _:
                    raise SyntaxError("Invalid Statement")

           

    def displaySymbolTable(self):
            print(self.symbol_table)

            

        




if "__main__" == __name__:

 
    
    parserObj = Parser.Parser("""
                       let x:int = 5;
                              
 
                     
                        for (let a:int = 0; a < 10; a = a + 1){
                           __print a
                        }
                              
                   
                    """)
    parserObj.Parse()

    print_visitor = ast.PrintNodesVisitor()
    parserObj.ASTroot.accept(print_visitor)
    sAnalyzer = SemanticAnalyzer(parserObj.ASTroot)
    sAnalyzer.analyze()
    sAnalyzer.displaySymbolTable()
