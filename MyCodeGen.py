

import Parser as Parser
import Lexer as lex
import SemanticAnalysis as sem
from ASTNodes import *
import ASTNodes as ast


# Used for checking for If, While or For nodes
keywordNodes = {ast.ASTIfNode, ast.ASTWhileNode, ast.ASTForNode}

class CodeGen(ASTVisitor):
    def __init__(self, program):
        # Instructions array holding final product
        self.instructions = ['.main']
        # Scope for function tracking
        self.currentScope = "main"
        # Symbol Table
        self.symbolTable = {}
        # Index 
        self.index = 0
        # Level
        self.level = -1
        # Code
        self.root = program

    def countInstructNum(self):
        '''Used to calculate how many instructions before a block evaluation (used for If, While and For statements)'''
        pass

    def countVariables(self, block):
        '''Used to calculate how many variables are in a block for memory allocation'''
        count = 0
        for x in block.stmts:
            if isinstance(x, ast.ASTAssignmentNode):
                # Allocate for variable
                count += 1
            elif isinstance(x, (ast.ASTForNode, ast.ASTWhileNode)):
                # Allocate for initial var i
                count += 1
                # Count necessary variables within block
                count += self.countVariables(x.block)

            elif isinstance(x, ast.ASTIfNode):
                # Count all variables within both if and else blocks
                count += self.countVariables(x.block)
                if x.elseBlock != None:
                    count += self.countVariables(x.elseBlock)

        return count

    def emit(self, ins):
        self.instructions.append(ins)
        self.index += 1


    def visit_integer_node(self, node):
        self.emit(f"push {node.value}")
    
    def visit_float_node(self, node):
        self.emit(node.value)

    # def visit_bool_node(self, node):

    def visit_assignment_node(self, node):
        # Assuming expressions are N Op N (none nested expressions)
        expr = node.expr
        expr.accept(self)

        if self.currentScope != "main":
            # Check if variable is in function scope
            if node.id.lexeme in self.symbolTable['functions'][self.currentScope]['symbolTable']:
                # retrieve variable 
                variable = self.symbolTable["functions"][self.currentScope]["symbolTable"][node.id.lexeme]
                # emit push
                self.emit(f"push {variable["index"]}")
                self.emit(f"push {variable["level"]}")
                self.emit('st')
            # Check if variable is in global scope
            elif node.id.lexeme in self.symbolTable.keys():
                # retrieve variable
                variable = self.symbolTable[node.id.lexeme]
                # emit push
                self.emit(f"push {variable["index"]}")
                self.emit(f"push {variable["level"]}")
                self.emit('st')

        else:
            # retrieve index
            index = self.symbolTable[node.id.lexeme]['index']
            # retrieve level
            level = self.symbolTable[node.id.lexeme]['level']
            self.emit(f'push {index}')
            self.emit(f'push {level}')
            self.emit('st')

    def visit_reassign_node(self, node):
        # evaluate expression
        node.expr.accept(self)

        if self.currentScope != "main":
            # Check if variable is in function scope
            if node.id.lexeme in self.symbolTable['functions'][self.currentScope]['symbolTable']:
                # retrieve variable
                variable = self.symbolTable["functions"][self.currentScope]["symbolTable"][node.id.lexeme]

                # emit push
                self.emit(f"push {variable["index"]}")
                self.emit(f"push {variable["level"]}")
                self.emit('st')
        else:
            # retrieve index
            index = self.symbolTable[node.id.lexeme]['index']
            # retrieve level
            level = self.symbolTable[node.id.lexeme]['level']
            self.emit(f'push {index}')
            self.emit(f'push {level}')
            self.emit('st')
    
    def visit_variable_node(self, node):
        # func variable incase variable is found in function block

        # If not, most definitely is in a function scope
        if self.currentScope != "main":  
            # Check if variable is in function scope
            if node.lexeme in self.symbolTable['functions'][self.currentScope]['symbolTable']:
                # retrieve variable 
                variable = self.symbolTable["functions"][self.currentScope]["symbolTable"][node.lexeme]
                # emit push
                # self.emit(f"push [{variable["index"]}:{variable["level"]}]")
                self.emit(f"push [{variable["index"]}:{variable['level'] + self.level}]")
            # Check if variable is in global scope
            elif node.lexeme in self.symbolTable.keys():
                # retrieve variable 
                variable = self.symbolTable[node.lexeme]
                # emit push
                # self.emit(f"push [{variable["index"]}:{variable["level"]}]")
                self.emit(f"push [{variable["index"]}:{variable['level'] + self.level}]")
        else:
            # Check if identifier is in global symbol table  
            if node.lexeme in self.symbolTable.keys():
                self.emit(f'push [{self.symbolTable[node.lexeme]['index']}:{self.symbolTable[node.lexeme]['level'] + self.level}]')
            else:
                raise SyntaxError(f"Variable {node.lexeme} is not defined.")

    def visit_return_node(self, node):
        node.expr.accept(self)
        self.emit('ret')
    # Made specifically for func blocks 
    def visit_func_block_node(self, node):
        # Open scope
        hasReturn = False
        # Allocate memory spaces for locals
        self.emit("alloc")
        
        # Iterate through each statement in func block
        for st in node.stmts:
            st.accept(self)
            self.index += 1

    def visit_func_node(self, node):
        # Set current scope to function name
        self.currentScope = node.name
        # Emit func name
        self.emit(f'.{node.name}')
        # Allocate space for parameters
        self.emit(f'push {self.countVariables(node.block) + len(node.params.params)}')

        # Custom visitor function specifically for node block
        self.visit_func_block_node(node.block)

    def visit_term_node(self, node):

        # List of multiplicative operators
        mulop = {"*" : "mul", "/" : "div", "and" : "and"}


        if node.right:
             # Visit right side
            node.right.accept(self)
            # Visit left side
            node.left.accept(self)
            # get operator
            op = mulop[node.mulop]
            self.emit(op)
        else:
            # Visit left side
            node.left.accept(self)

    def visit_simpleexp_node(self, node):
        # List of additive operators
        addop = {"+" : "add", "-" : "sub", "or" : "or"}
        if node.right:
            # Visit right side
            node.right.accept(self)
            # Visit left side
            node.left.accept(self)

            # get operator
            op = addop[node.adop]
            self.emit(op)
        else:
            node.left.accept(self)

    def visit_while_node(self, node):
        # Calculate pushback (for loop imlpementation)
        cur_instrs = self.instructions.copy()
        # visit conditional expression
        node.expr.accept(self)

        pushback1 = len(self.instructions) - len(cur_instrs)

        # Get current instructions again before processing while block
        cur_instrs = self.instructions.copy()

        # visit then block
        node.block.accept(self)

        # Get length difference between new and old instructions for skip
        instruct_diff_no = len(self.instructions) - len(cur_instrs)
        
        # 2 includes the last instructions (cjmp & push #PC+WhileBlockInstructs)
        pushback2 = pushback1 + instruct_diff_no + 2

        # to skip incase if false (inserted before the blocks)
        self.instructions.insert(len(cur_instrs), f'cjmp')
        self.instructions.insert(len(cur_instrs), f'push #PC+{instruct_diff_no}')

        # Push back instruction for loop
        self.instructions.append(f'push #PC-{pushback2}')
        self.instructions.append(f'jmp')

    def visit_if_node(self, node):
        # visit conditional expression
        node.conds.accept(self)

        # Get current instructions before processing if block
        cur_instrs = self.instructions.copy()

        # visit then block
        self.emit('oframe')
        node.block.accept(self)
        self.emit('cframe')

        # Get length difference between new and old instructions for skip
        instruct_diff_no = len(self.instructions) - len(cur_instrs)
            
        # to skip incase if false (inserted before the blocks)  
        # Jump to if true block (Always is 4)

        self.instructions.insert(len(cur_instrs), f'jmp')
        self.instructions.insert(len(cur_instrs), f'push #PC+{instruct_diff_no + 1}')  
 
        if node.elseBlock != None:
            # Same procedure but for else block
            cur_instrs = self.instructions.copy()
            self.instructions.insert(len(cur_instrs), f'jmp')

            node.elseBlock.accept(self)

            instruct_diff_no = len(self.instructions) - len(cur_instrs)

            self.instructions.insert(len(cur_instrs), f'push #PC+{instruct_diff_no + 1}')
        else:
            self.instructions.insert(len(cur_instrs), f'cjmp')
            self.instructions.insert(len(cur_instrs), f'push #PC+4')        
            
    def visit_exp_node(self, node):
        # Reloperators
        relop = {"<" : "lt", ">" : "gt", "<=" : "le", ">=" : "ge", "==" : "eq"}
        # if node.right exists
        if node.right:
            # visit right first
            node.right.accept(self)
            # visit left first
            node.left.accept(self)
         
            op = relop[node.op]
            self.emit(op)
        else:
            # visit left first
            node.left.accept(self)


        # # Visit lhs 
        # node.left.accept(self)

        # # If rhs exists, visit it
        # if node.right:
        #     node.right.accept(self)
        #     op = relop[node.op]
        #     self.emit(op)

    def visit_for_node(self, node):
        self.emit(f'push {self.countVariables(node.block) + 1}')
        self.oFrame()
        # Visit Initialization
        node.init.accept(self)

        # Record instructions before condition statements
        beforeCondition = self.instructions.copy()
        # Visit Condition
        node.cond.accept(self)
        # Record instruction length difference after condition statements
        afterCondition = len(self.instructions) - len(beforeCondition) 


        # Get current instructions before processing for block

        count = self.countVariables(node.block)
        self.emit(f"push {count}")
        self.emit(f"oframe")
        # Insert before block
        self.emit('push #PC+4')  
        self.emit('cjmp')
        cur_instrs = self.instructions.copy()


        # Visit Block  
 
        self.oFrame()
        node.block.accept(self)
        

        self.cFrame()
        
        # Process step expression
        node.step.accept(self)  
        
        # Get new difference between new and old instructions for pushback
        pushback = len(self.instructions) - len(beforeCondition) - 1

        
        self.emit(f'push #PC-{pushback + afterCondition}')
        self.emit('jmp')  
        self.cFrame()  

        # Get length difference between new and old instructions for skip
        instruct_diff_no = len(self.instructions) - len(cur_instrs)

        self.instructions.insert(len(cur_instrs), f'jmp')
        self.instructions.insert(len(cur_instrs), f'push #PC+{instruct_diff_no + 2}')  

    def visit_print_node(self, node):
        print(self.instructions)
        node.expr.accept(self)
        print(self.instructions)
        self.emit('print')

    def visit_actualparams_node(self, node):
        # Invert params
        tempParams = node.params[::-1]
  
        # visit each param
        for x in tempParams:
            x.accept(self)
    
    def visit_func_call(self, node):
        # Visit parameter inputs
        node.params.accept(self)
        # Check node symbol table


        funcSymbolTable = self.symbolTable['functions'][node.name]['symbolTable']
        if len(funcSymbolTable) > 0:
            self.emit(f'push {len(funcSymbolTable)}')

        # Push function into stack
        self.emit(f'push .{node.name}')
        # call function
        self.emit(f'call ')

    def visit_writeBox_node(self, node):
        # __writeBox x, y, width, height, color
        self.emit(f'push {node.color}')
        self.emit(f'push {node.y}')
        self.emit(f'push {node.x}')
        self.emit(f'push {node.v.accept(self)}')
        self.emit(f'push {node.u.accept(self)}')
 
       
        
        self.emit('writebox')
   
    def visit_bool_node(self, node):
        if node.value == "true":

            self.emit("push 1")
        
        elif node.value == "false":

            self.emit("push 0")

    def visit_declare_node(self, node): 
        node.var.accept(self)
        
    def visit_block_node(self, node):
        ins_count = 0
        hasReturn = False
        # function arrays, as Main block is to be processed first, then the rest.
        functions = []
        for st in node.stmts:
            print(st)
            # If function
            if isinstance(st, ast.ASTFunctionNode):
                # append

                functions.append(st)
                # Go next statement
                self.index += 1
                continue
            # If return node
            if isinstance(st, ast.ASTReturnNode):
                # Visit return expression
                st.expr.accept(self)
                # Set return to true
                hasReturn = True
                self.index += 1
                continue

            st.accept(self)
            self.index += 1

        # If functions are defined (this will ever only be the case within the main block)
        if len(functions) > 0:
                self.emit("halt")
                for func in functions:
                    func.accept(self)

        if hasReturn:
            self.emit("ret")
    def visit_height_node(self, node):
        self.emit('height')
    
    def visit_width_node(self, node):
        self.emit('width')
    def visit_program_node(self):
        # Loop through code
        block = self.root.block
        # Allocate space for block
        count = self.countVariables(block)
        self.emit(f"push {count}")
        # Open scope
        self.oFrame()
        block.accept(self)
        self.cFrame()
        self.emit('halt')

        for ins in self.instructions:
            print(ins)
                    

    def oFrame(self):
        self.emit("oframe")
        self.level += 1

    def cFrame(self):
        self.emit("cframe")
        self.level -= 1

# __write_box x, x, 1, 1, #0000ff;

if __name__ == "__main__":
    parserObj = Parser.Parser("""
                        let x:int = 5;
                              
 
                     
                        for (let a:int = 0; a < 10; a = a + 1){
                           __print a
                        }
 
                              
                    """)
    parserObj.Parse()

    print_visitor = ast.PrintNodesVisitor()
    parserObj.ASTroot.accept(print_visitor)
    sAnalyzer = sem.SemanticAnalyzer(parserObj.ASTroot)
    sAnalyzer.analyze()
    codeGen = CodeGen(parserObj.ASTroot)
    codeGen.symbolTable = sAnalyzer.symbol_table
    print(codeGen.symbolTable)
    codeGen.visit_program_node()


