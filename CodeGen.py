import Parser as Parser
import Lexer as lex
import SemanticAnalysis as sem
import ASTNodes as ast

class CodeGen(ast.ASTVisitor):
    def __init__(self):
        super().__init__()
        self.opStack = []
        self.addressStack = {}
        self.instructions = []
        self.pIndex = 0
        self.memory = []
        self.program = [".main"]
        self.current_function = None

    def emit(self, instruction):
        self.instructions.append(instruction)
        self.pIndex += 1

    def visit_program_node(self, node):
        # Visit the main block
        node.block.accept(self)
        # Emit halt at the end of main
        self.emit("halt")

    def visit_func_node(self, node):
        funcName = node.name
        self.addressStack[funcName] = self.pIndex
        self.program.append(f".{funcName}")
        self.current_function = funcName
        # Open a new frame for the function
        self.oFrame()
        # Visit function block
        if node.block:
            node.block.accept(self)
        # Close the frame
        self.cFrame()
        # Emit ret instruction at function end
        self.emit("ret")
        self.current_function = None

    def visit_block_node(self, node):
        for stmt in node.stmts:
            stmt.accept(self)

    def visit_integer_node(self, node):
        # push integer value
        self.emit(f"push {node.value}")

    def visit_colour_node(self, node):
        # push colour encoded as integer
        # Assuming colour is a hex string like #00ff00, convert to int
        colour_int = int(node.colour.lstrip('#'), 16)
        self.emit(f"push {colour_int}")

    def visit_variable_node(self, node):
        # push variable value from stack frame
        # For simplicity, assume variable name maps to some index
        # Here we just push a placeholder address (to be improved)
        self.emit(f"push [0:0]  # variable {node.lexeme}")

    def visit_assignment_node(self, node):
        # Evaluate expression and assign to variable
        node.expr.accept(self)
        # For simplicity, assume variable index 0 and level 0
        self.emit("st 0 0")

    def visit_reassign_node(self, node):
        # Similar to assignment
        node.expr.accept(self)
        self.emit("st 0 0")

    def visit_exp_node(self, node):
        # Visit left and right expressions
        if node.left:
            node.left.accept(self)
        if node.right:
            node.right.accept(self)
        # Emit operation based on node.op
        op_map = {
            '+': 'add',
            '-': 'sub',
            '*': 'mul',
            '/': 'div',
            '%': 'mod',
            '==': 'eq',
            '<': 'lt',
            '<=': 'le',
            '>': 'gt',
            '>=': 'ge',
            '&&': 'and',
            '||': 'or',
        }
        if node.op in op_map:
            self.emit(op_map[node.op])
        else:
            # No operation or unknown
            pass

    def visit_return_node(self, node):
        if node.expr:
            node.expr.accept(self)
        self.emit("ret")

    def visit_if_node(self, node):
        # Evaluate condition
        node.conds.accept(self)
        # Emit conditional jump placeholder
        jmp_false_index = self.pIndex
        self.emit("cjmp 0 0 0")  # placeholder
        # Visit if block
        node.block.accept(self)
        # Emit jump over else block
        jmp_end_index = self.pIndex
        self.emit("jmp 0")
        # Fix cjmp to jump here if false
        self.instructions[jmp_false_index] = f"cjmp {self.pIndex} 0 0"
        # Visit else block if present
        if node.elseBlock:
            node.elseBlock.accept(self)
        # Fix jmp to jump here
        self.instructions[jmp_end_index] = f"jmp {self.pIndex}"

    def visit_while_node(self, node):
        loop_start = self.pIndex
        node.expr.accept(self)
        jmp_false_index = self.pIndex
        self.emit("cjmp 0 0 0")  # placeholder
        node.block.accept(self)
        self.emit(f"jmp {loop_start}")
        self.instructions[jmp_false_index] = f"cjmp {self.pIndex} 0 0"

    def visit_for_node(self, node):
        # For loop: init; cond; step; block
        node.init.accept(self)
        loop_start = self.pIndex
        node.cond.accept(self)
        jmp_false_index = self.pIndex
        self.emit("cjmp 0 0 0")  # placeholder
        node.block.accept(self)
        node.step.accept(self)
        self.emit(f"jmp {loop_start}")
        self.instructions[jmp_false_index] = f"cjmp {self.pIndex} 0 0"

    def visit_print_node(self, node):
        node.expr.accept(self)
        self.emit("print")

    def visit_write_node(self, node):
        node.u.accept(self)
        node.v.accept(self)
        node.color.accept(self)
        self.emit("write")

    def visit_writeBox_node(self, node):
        node.u.accept(self)
        node.v.accept(self)
        node.x.accept(self)
        node.y.accept(self)
        node.color.accept(self)
        self.emit("writebox")

    def visit_delay_node(self, node):
        node.expr.accept(self)
        self.emit("delay")

    def visit_bool_node(self, node):
        val = 1 if node.value else 0
        self.emit(f"push {val}")

    def visit_float_node(self, node):
        # For simplicity, treat float as integer by truncation
        self.emit(f"push {int(node.value)}")

    def visit_string_node(self, node):
        # Strings not supported in VM, skip or implement as needed
        pass

    def visit_unary_node(self, node):
        # Handle unary operators like inc, dec, not
        node.expr.accept(self)
        op_map = {
            '++': 'inc',
            '--': 'dec',
            '!': 'not',
        }
        if node.lexeme in op_map:
            self.emit(op_map[node.lexeme])

    def visit_term_node(self, node):
        # Similar to exp node but for multiplicative ops
        if node.left:
            node.left.accept(self)
        if node.right:
            node.right.accept(self)
        op_map = {
            '*': 'mul',
            '/': 'div',
            '%': 'mod',
        }
        if node.mulop in op_map:
            self.emit(op_map[node.mulop])

    def visit_actualparams_node(self, node):
        for param in node.params:
            param.accept(self)

    def visit_func_call(self, node):
        # Push function address if known
        if node.name in self.addressStack:
            self.emit(f"push .{node.name}")
        # Push actual parameters
        if node.params:
            node.params.accept(self)
        # Call function
        self.emit("call")

    def visit_declare_node(self, node):
        # For variable declaration, no code needed here
        pass

    def oFrame(self):
        # Open a new frame with space for variables
        # For simplicity, allocate a fixed size frame (e.g., 10 variables)
        self.emit("oframe 10")

    def cFrame(self):
        # Close the current frame
        self.emit("cframe")

    def mainExec(self):
        # Entry point to generate code from AST root
        pass

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
