

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

        # Symbol Table
        self.symbolTable = {}
        # Index 
        self.index = 0
        # Level
        self.level = 0
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

        # retrieve index
        index = self.symbolTable[node.id.lexeme]['index']
        # retrieve level
        level = self.symbolTable[node.id.lexeme]['level']
        self.emit(f'push {index}')
        self.emit(f'push {level}')
        self.emit('st')
    
    def visit_variable_node(self, node):
        # Check if identifier is in symbol table    
        if node.lexeme in self.symbolTable.keys():
            self.emit(f'push [{self.symbolTable[node.lexeme]['index']}:{self.symbolTable[node.lexeme]['level']}]')
        else:
            raise SyntaxError(f"Variable {node.lexeme} is not defined.")
    def visit_return_node(self, node):
        node.expr.accept(self)
        self.emit('ret')
    # Made specifically for func blocks 
    def visit_func_block_node(self, node):
        # Open scope
        hasReturn = False
        self.emit("oframe")
        # Iterate through each statement in func block
        for st in node.stmts:
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
        self.emit("cframe")
        if hasReturn:
            self.emit("ret")

    def visit_func_node(self, node):
        # Emit func name
        self.emit(f'.{node.name}')
        # Allocate space for parameters
        self.emit(f'push {len(node.params.params) + self.countVariables(node.block)}')

        # Custom visitor function specifically for node block
        self.visit_func_block_node(node.block)

    def visit_term_node(self, node):
        # Visit left side
        node.left.accept(self)
        # Visit right side
        node.right.accept(self)
        # List of multiplicative operators
        mulop = {"*" : "mul", "/" : "div", "and" : "and"}

        # get operator
        op = mulop[node.mulop]
        self.emit(op)

    def visit_simpleexp_node(self, node):
        # Visit left side
        node.left.accept(self)
        # Visit right side
        node.right.accept(self)
        # List of additive operators
        addop = {"+" : "add", "-" : "sub", "or" : "or"}

        # get operator
        op = addop[node.adop]
        self.emit(op)

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
        node.block.accept(self)

        # Get length difference between new and old instructions for skip
        instruct_diff_no = len(self.instructions) - len(cur_instrs)
            
        # to skip incase if false (inserted before the blocks)
        self.instructions.insert(len(cur_instrs), f'cjmp')
        self.instructions.insert(len(cur_instrs), f'push #PC+{instruct_diff_no}')
 
        if node.elseBlock != None:
            # Same procedure but for else block
            cur_instrs = self.instructions.copy()

            node.elseBlock.accept(self)

            instruct_diff_no = len(self.instructions) - len(cur_instrs)

            self.instructions.insert(len(cur_instrs), f'jmp')
            self.instructions.insert(len(cur_instrs), f'push #PC+{instruct_diff_no}')

    def visit_exp_node(self, node):
        # Reloperators
        relop = {"<" : "lt", ">" : "gt", "<=" : "le", ">=" : "ge", "==" : "eq"}
        
        # Visit lhs 
        node.left.accept(self)

        # If rhs exists, visit it
        if node.right:
            node.right.accept(self)
            op = relop[node.op]
            self.emit(op)

    def visit_for_node(self, node):
        # Visit Initialization
        node.init.accept(self)

        # Visit Condition
        node.cond.accept(self)

        # Get current instructions before processing for block
        cur_instrs = self.instructions.copy()

        # Visit Block
        node.block.accept(self)

        # Get length difference between new and old instructions for skip
        instruct_diff_no = len(self.instructions) - len(cur_instrs)

        # Insert before block 
        self.instructions.insert(len(cur_instrs), f'cjmp')
        self.instructions.insert(len(cur_instrs), f'push #PC+{instruct_diff_no}')
        



        # Process step expression
        node.step.accept(self)
        # Get new difference between new and old instructions for pushback
        pushback = len(self.instructions) - len(cur_instrs)
        
        self.emit(f'push #PC+{pushback}')
        self.emit('jmp')        

    def visit_print_node(self, node):
        node.expr.accept(self)
        self.emit('print')

    def visit_actualparams_node(self, node):
        pass
    
    def visit_bool_node(self, node):
        if node.value == "true":
            self.emit("push 1")
        elif node.value == "false":
            self.emit("push 0")
    def visit_block_node(self, node):
        ins_count = 0
        hasReturn = False
        # Allocate space for block
        count = self.countVariables(node)
        self.emit(f"push {count}")

        # Open scope
        self.emit("oframe")
        for st in node.stmts:
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
        self.emit("cframe")
        if hasReturn:
            self.emit("ret")

    def visit_program_node(self):
        # Loop through code
        block = self.root.block
        block.accept(self)

        self.emit("halt")
        

        # while self.index < len(Block):
        #     currentNode = Block[self.index] 

        #     match type(currentNode):
        #         case ast.ASTAssignmentNode:
        #             self.visit_assignment_node(currentNode)

        for ins in self.instructions:
            print(ins)
                    




if __name__ == "__main__":
    parserObj = Parser.Parser("""
                    let x:int = 259;
                    fun test(a:int) -> bool{
                        if ( x > 50) {
                            x = 50;
                        }
                    }
                              
                    """)
    parserObj.Parse()

    # print_visitor = ast.PrintNodesVisitor()s
    # parserObj.ASTroot.accept(print_visitor)
    sAnalyzer = sem.SemanticAnalyzer(parserObj.ASTroot)
    sAnalyzer.analyze()
    codeGen = CodeGen(parserObj.ASTroot)
    codeGen.symbolTable = sAnalyzer.symbol_table
    print(codeGen.symbolTable)
    codeGen.visit_program_node()


