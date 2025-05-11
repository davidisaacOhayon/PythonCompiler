
import Lexer as lex

#First some AST Node classes we'll use to build the AST with
class ASTNode:
    def __init__(self):
        self.name = "ASTNode"    
class ASTProgramNode(ASTNode):
    def __init__(self, block):
        self.name = "ASTProgramNode"
        self.block = block
    
    def accept(self, visitor):
        visitor.visit_program_node(self)

class ASTStatementNode(ASTNode):
    def __init__(self):
        self.name = "ASTStatementNode"

class ASTExpressionNode(ASTNode):
    def __init__(self):
        self.name = "ASTExpressionNode"
        self.type = None

class ASTVariableNode(ASTExpressionNode):
    def __init__(self, lexeme):
        self.name = "ASTVariableNode"
        self.lexeme = lexeme

    def accept(self, visitor):
        visitor.visit_variable_node(self)

class ASTUnaryNode(ASTExpressionNode):
    def __init__(self, lexeme):
        self.name = "ASTUnaryNode"
        self.lexeme = lexeme

    def accept(self, visitor):
        visitor.visit_unary_node(self)

class ASTFactorNode(ASTExpressionNode):
    def __init__(self, lexeme, type):
        self.name = "ASTFactorNode"
        self.lexeme = lexeme
        self.type = type
    
    def accept(self, visitor):
        visitor.visit_factor_node(self)

class ASTSimpleExpNode(ASTExpressionNode):
    def __init__(self, lhs, adop=None, rhs=None, type = None):
        self.name = "ASTAdopNode"
        self.adop = adop
        self.left = lhs 
        self.right = rhs
        self.type = type
    
    def accept(self, visitor):
        visitor.visit_simpleexp_node(self)

class ASTExpNode(ASTExpressionNode):
    def __init__(self, lhs, type=None, op=None, rhs=None):
        self.name = "ASTExpNode"
        self.op = op
        self.left = lhs
        self.right = rhs
        self.type = type

    def accept(self,visitor):
        visitor.visit_exp_node(self)

class ASTDeclareNode(ASTNode):
    def __init__(self, var, type):
        self.name = "ASTDeclareNode"
        self.var = var
        self.type = type
    
    def accept(self, visitor):
        visitor.visit_declare_node(self)

class ASTReturnNode(ASTNode):
    def __init__(self, expr, type):
        self.name = "ASTReturnNode"
        self.expr = expr
        self.type = type
    
    def accept(self, visitor):
        visitor.visit_return_node(self)

class ASTIfNode(ASTNode):
    def __init__(self, conds, block, elseBlock = None):
        self.name = "ASTIfNode"
        self.conds = conds
        self.block = block
        self.elseBlock = elseBlock
    
    def accept(self, visitor):
        visitor.visit_if_node(self)
        
class ASTForNode(ASTNode):
    def __init__(self, init, cond, step, block=None):
        self.name = "ASTForNode"
        self.init = init
        self.cond = cond
        self.step = step
        self.block = block
    
    def accept(self, visitor):
        visitor.visit_for_node(self)

class ASTWhileNode(ASTNode):
    def __init__(self, expr, block):
        self.name = "ASTWhileNode"
        self.expr = expr
        self.block = block

    def accept(self, visitor):
        visitor.visit_while_node(self)

class ASTWidthNode(ASTExpressionNode):
    def __init__(self):
        self.name = "ASTWidthNode"
        self.type = lex.TokenType.Integer
    
    def accept(self, visitor):
        visitor.visit_width_node(self)

class ASTHeightNode(ASTExpressionNode):
    def __init__(self):
        self.name = "ASTHeightNode"
        self.type = lex.TokenType.Integer
    
    def accept(self, visitor):
        visitor.visit_height_node(self)

class ASTReadNode(ASTNode):
    def __init__(self, expr):
        self.name = "ASTWidthNode"
    
    def accept(self, visitor):
        visitor.visit_height_node(self)

class ASTHeightNode(ASTNode):
    def __init__(self):
        self.name = "ASTWidthNode"
    
    def accept(self, visitor):
        visitor.visit_height_node(self)

class ASTDelayNode(ASTNode):
    def __init__(self, val):
          self.name = "ASTDelayNode"
          self.expr = val
    def accept(self, visitor):
          visitor.visit_delay_node(self)

class ASTWriteBoxNode(ASTNode):
    def __init__(self, u, v, x, y, color):
          self.name = "ASTWriteBoxNode"
          self.u, self.v = u, v
          self.x, self.y = x, y
          self.color = color

    def accept(self, visitor):
          visitor.visit_writeBox_node(self)

class ASTWriteNode(ASTNode):
    def __init__(self, u, v, color):
          self.name = "ASTWriteNode"
          self.u, self.v = u, v
          self.color = color

    def accept(self, visitor):
          visitor.visit_write_node(self)

class ASTPrintNode(ASTNode):
      def __init__(self, expr):
          self.name = "ASTPrintNode"
          self.expr = expr
      def accept(self, visitor):
          visitor.visit_print_node(self)

class ASTTermNode(ASTExpressionNode):
    def __init__(self, lhs, mulop=None, rhs=None, type=None):
        self.name = "ASTTermNode"
        self.mulop = mulop
        self.left = lhs 
        self.right = rhs
        self.type = type
        
    def accept(self, visitor):
        visitor.visit_term_node(self)

class ASTIntegerNode(ASTExpressionNode):
    def __init__(self, v):
        self.name = "ASTIntegerNode"
        self.value = v
        self.type = lex.TokenType.Integer
    def accept(self, visitor):
        visitor.visit_integer_node(self)   

class ASTColourNode(ASTExpressionNode):
    def __init__(self, colour):
        self.name = "ASTColourNode"
        self.colour = colour
        self.type = lex.TokenType.ColourLiteral

    def accept(self, visitor):
        visitor.visit_colour_node(self)

class ASTFloatNode(ASTExpressionNode):
    def __init__(self,v):
        self.name = 'ASTFloatNode'
        self.value = v  
        self.type = lex.TokenType.FloatLiteral 
    
    def accept(self, visitor):
        visitor.visit_float_node(self)

class ASTBoolNode(ASTExpressionNode):
    def __init__(self, v : bool):
        self.name = "ASTBoolNode"
        self.value = v
        self.type = lex.TokenType.BooleanLiteral 

    def accept(self, visitor):
        visitor.visit_bool_node(self)

class ASTStringNode(ASTExpressionNode):
    def __init__ (self, string):
        self.name = "ASTStringNode"
        self.string = string 
        self.type = lex.TokenType.String
    
    def accept(self, visitor):
        visitor.visit_string_node(self)
 
class ASTAssignmentNode(ASTNode):
    def __init__(self, id, ast_expression_node):
        self.name = "ASTAssignmentNode"        
        self.id   = id
        self.expr = ast_expression_node

    def accept(self, visitor):
        visitor.visit_assignment_node(self)       

class ASTReAssignNode(ASTNode):
    def __init__(self, id, expr):
        self.name = "ASTReAssignNode"
        self.id = id
        self.expr = expr
    
    def accept(self, visitor):
        visitor.visit_reassign_node(self)
         

class ASTActualParamsNode(ASTNode):
    def __init__(self):
        self.name = 'ASTActualParamsNode'
        self.params = []

    def add_params(self, param):
        self.params.append(param)
    
    def accept(self, visitor):  
        visitor.visit_actual_params_node(self)

class ASTFormalParamNode(ASTNode):
    def __init__(self, var, type):
        self.name = "ASTFormalParamNode"
        self.var = var
        self.type = type
    
    def accept(self, visitor):
        visitor.visit_formalparam_node(self)

class ASTFormalParamsNode(ASTNode):
    def __init__(self):
        self.name = 'ASTActualParamsNode'
        self.params = []

    def add_params(self, param):
        self.params.append(param)
    
    def accept(self, visitor):  
        visitor.visit_formalparams_node(self)

class ASTFunctionNode(ASTNode):
    def __init__(self, name=None, params= ASTFormalParamsNode() ):
        self.name = "ASTFunctionNode"
        # ASTFormalParams
        self.params = params
        self.returnType = None
        self.block : ASTBlockNode = None

    def accept_params(self, visitor):
        for x in self.params:
            x.accept(visitor)

    def accept(self, visitor):
        visitor.visit_func_node(self)

class ASTFunctionCall(ASTNode):
    def __init__(self, params = None):
        self.name = "ASTFunctionCall"
        self.params = params

    def accept(self, visitor):
        visitor.visit_func_call(self)

class ASTBlockNode(ASTNode):
    def __init__(self):
        self.name = "ASTBlockNode"
        self.stmts = []

    def add_statement(self, node):
        self.stmts.append(node)

    def accept(self, visitor):
        visitor.visit_block_node(self)   

class ASTVisitor:
    def visit_integer_node(self, node):
        raise NotImplementedError()

    def visit_assignment_node(self, node):
        raise NotImplementedError()
    
    def visit_reassign_node(self, node):
        raise NotImplementedError()
    
    def visit_program_node(self,node):
        raise NotImplementedError()
    
    def visit_term_node(self, node):
        raise NotImplementedError()
    
    def visit_simpleexp_node(self,node):
        raise NotImplementedError()
    
    def visit_variable_node(self, node):
        raise NotImplementedError()
    
    def visit_block_node(self, node):
        raise NotImplementedError()
    
    def visit_float_node(self, node):
        raise NotImplementedError()
    
    def visit_actualparams_node(self, node):
        raise NotImplementedError()
    
    def visit_formalparams_node(self, node):
        raise NotImplementedError()
    
    def visit_unary_node(self, node):
        raise NotImplementedError()
    
    def visit_factor_node(self, node):
        raise NotImplementedError()
    
    def visit_func_node(self, node):
        raise NotImplementedError()

    def visit_func_call(self, node):
        raise NotImplementedError()
    
    def visit_exp_node(self, node):
        raise NotImplementedError()
    
    def visit_string_node(self, node):
        raise NotImplementedError()
    
    def visit_colour_node(self, node):
        raise NotImplementedError()
    
    def visit_width_node(self, node):
        raise NotImplementedError()
    
    def visit_height_node(self, node):
        raise NotImplementedError()
    
    def visit_read_node(self, node):
        raise NotImplementedError()
    
    def visit_delay_node(self, node):
        raise NotImplementedError()
    
    def visit_print_node(self, node):
        raise NotImplementedError()
    
    def visit_writeBox_node(self, node):
        raise NotImplementedError()
    
    def visit_write_node(self, node):
        raise NotImplementedError()
    
    def visit_rand_node(self, node):
        raise NotImplementedError()
    
    def visit_bool_node(self, node):
        raise NotImplementedError()
    
    def inc_tab_count(self):
        raise NotImplementedError()
    
    def dec_tab_count(self):
        raise NotImplementedError()
    
    def visit_declare_node(self):
        raise NotImplementedError()
    
    def visit_if_node(self):
        raise NotImplementedError()
    
    def visit_while_node(self):
        raise NotImplementedError()
    
    def visit_for_node(self):
        raise NotImplementedError()

class PrintNodesVisitor(ASTVisitor):
    def __init__(self):
        self.name = "Print Tree Visitor"
        self.node_count = 0
        self.tab_count = 0

    def inc_tab_count(self):
        self.tab_count += 1

    def visit_program_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "Program Node => ")
        self.inc_tab_count()
        node.block.accept(self)
        self.dec_tab_count()

    def dec_tab_count(self):
        self.tab_count -= 1
        
    def visit_integer_node(self, int_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Integer value::", int_node.value)

    def visit_float_node(self, float_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Float value::", float_node.value)

    def visit_func_node(self, func_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Function name::", func_node.name)
        print('\t' * self.tab_count, "Parameters:: ")
        func_node.params.accept(self)
        print('\t' * self.tab_count, "Return Type:: ", func_node.returnType)
        self.visit_block_node(func_node.block)

    def visit_func_call(self, func_call):
        self.node_count += 1
        print('\t' * self.tab_count, "Function Call =>")
        self.inc_tab_count()
        print('\t' * self.tab_count, "Function Name ::", func_call.name)
        print('\t' * self.tab_count, "Arguments:: ")
        self.inc_tab_count()
        for arg in func_call.params:
            arg.accept(self)
        self.dec_tab_count()
   
    def visit_bool_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "Boolean value::", node.value)
        
    def visit_assignment_node(self, ass_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Assignment node => ")
        self.inc_tab_count()        
        ass_node.id.accept(self)
        ass_node.expr.accept(self)
        self.dec_tab_count()

    def visit_reassign_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "Reassignment node => ")
        self.inc_tab_count()        
        node.id.accept(self)
        node.expr.accept(self)
        self.dec_tab_count()
 
    def visit_width_node(self, node):
        self.node_count += 1
        self.inc_tab_count()    
        print('\t' * self.tab_count, "Width Constant")
        self.dec_tab_count()

    def visit_height_node(self, node):
        self.node_count += 1
        self.inc_tab_count()    
        print('\t' * self.tab_count, "Height Constant")
        self.dec_tab_count()

    def visit_read_node(self, node):
        self.node_count += 1
        self.inc_tab_count()    
        print('\t' * self.tab_count, "Read node")
        self.dec_tab_count()

    def visit_print_node(self, node):
        self.node_count += 1
        self.inc_tab_count()    
        print('\t' * self.tab_count, "Print Node =>")
        self.inc_tab_count()
        node.expr.accept(self)
        self.dec_tab_count()

    def visit_read_node(self, node):
        self.node_count += 1
        self.inc_tab_count()    
        print('\t' * self.tab_count, "Delay node :: ", node.val)
        self.dec_tab_count()

    def visit_write_node(self, node):
        self.node_count += 1
        self.inc_tab_count()    
        print('\t' * self.tab_count, "Write node =>")
        self.inc_tab_count()   
        print('\t' * self.tab_count, "pos u ::", node.u)
        print('\t' * self.tab_count, "pos v ::", node.v)
        print('\t' * self.tab_count, "color::", node.color)
        self.dec_tab_count()

    def visit_writeBox_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "Write Box node =>")
        self.inc_tab_count()   
        print('\t' * self.tab_count, "pos u ::", node.u)
        print('\t' * self.tab_count, "pos v ::", node.v)
        print('\t' * self.tab_count, "size x ::", node.x)
        print('\t' * self.tab_count, "size y ::", node.y)    
        print('\t' * self.tab_count, "color::", node.color)
        self.dec_tab_count()

    def visit_unary_node(self, node):
        pass

    def visit_string_node(self, node):
        self.node_count += 1
        self.inc_tab_count()
        print('\t' * self.tab_count, "String Value:: ", self.node.string)
        self.dec_tab_count()

    def visit_declare_node(self,node):
        self.node_count += 1
        print('\t' * self.tab_count, "Declare node => ")
        self.inc_tab_count()
        print('\t' * self.tab_count, "Type:: ", node.type)
        node.var.accept(self)
        self.dec_tab_count()
        
    def visit_colour_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "Colour value::", node.colour)

    def visit_term_node(self, node):
        self.node_count += 1
        # If not a singular factor
        # if node.mulop and node.left and node.right:
        print('\t' * self.tab_count, "Multiplicative Operator => ", node.mulop)
        self.inc_tab_count()
        print('\t' * self.tab_count, 'left')
        node.left.accept(self)
        print('\t' * self.tab_count, 'right')
        node.right.accept(self)
        self.dec_tab_count()
        # else:
        #     self.inc_tab_count()
        #     node.left.accept(self)
        #     self.dec_tab_count()

    def visit_return_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "Return node => ")
        self.inc_tab_count()
        print('\t' * self.tab_count, "Return Type ::  ", node.type)
        node.expr.accept(self)
        self.dec_tab_count()
    
    def visit_for_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "For node => ")
        self.inc_tab_count()
        print('\t' * self.tab_count, "Initialization::")
        self.inc_tab_count()
        node.init.accept(self)
        self.dec_tab_count()
        print('\t' * self.tab_count, "Condition::")
        self.inc_tab_count()
        node.cond.accept(self)
        self.dec_tab_count()
        print('\t' * self.tab_count, "Step::")
        self.inc_tab_count()
        node.step.accept(self)
        self.dec_tab_count()
        print('\t' * self.tab_count, "Block::")
        self.inc_tab_count()
        node.block.accept(self)
        self.dec_tab_count()

    def visit_while_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "While Node =>")
        print('\t' * self.tab_count, "Conditions:: ")
        self.inc_tab_count()
        node.expr.accept(self)
        self.dec_tab_count()
        node.block.accept(self)

    def visit_if_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "If Node =>")
        print('\t' * self.tab_count, "Conditions:: ")
        self.inc_tab_count()
        node.conds.accept(self)
        node.block.accept(self)
        
        if node.elseBlock:
            print('\t' * self.tab_count, "Else:: ")
            node.elseBlock.accept(self)
        self.dec_tab_count()
        
    def visit_simpleexp_node(self, node):
        self.node_count += 1
        # If not a singular Term
        if node and node.left and node.right:
            print('\t' * self.tab_count, "Additive Operator => ", node.adop)
            self.inc_tab_count()
            print('\t' * self.tab_count, 'left')
            node.left.accept(self)
            print('\t' * self.tab_count, 'right')
            node.right.accept(self)
            self.dec_tab_count()
        # Print left single Term
        else:
            self.inc_tab_count()
            node.left.accept(self)
            self.dec_tab_count()

    def visit_exp_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "Expression Node =>")
        # print('\t' * self.tab_count, "of Type : ", node.type)
        if node and node.left and node.right:
            print('\t' * self.tab_count, "Expression Operator:: ", node.op)
            self.inc_tab_count()
            print('\t' * self.tab_count, 'left')
            node.left.accept(self)
            print('\t' * self.tab_count, 'right')
            node.right.accept(self)
            self.dec_tab_count()
        else:
            self.inc_tab_count()
            node.left.accept(self)
            self.dec_tab_count()

    def visit_actualparams_node(self, node):
        self.node_count += 1
        self.inc_tab_count()

    def visit_formalparams_node(self, node):
        self.node_count += 1
        self.inc_tab_count()
        print('\t' * self.tab_count, "Formal Parameters =>")
        self.inc_tab_count()
        for param in node.params:
            param.accept(self)
        self.dec_tab_count()
        self.dec_tab_count()

        

    
    def visit_formalparam_node(self, node):
        self.node_count += 1
        self.inc_tab_count()
        print('\t' * self.tab_count, "Formal Parameter :: ", node.var, " Type ::" , node.type)
        self.dec_tab_count()


    def visit_factor_node(self, node):
        self.node_count += 1
        self.inc_tab_count()
        node.lexeme.accept(self)

    def visit_variable_node(self, var_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Variable => ", var_node.lexeme)

    def visit_block_node(self, block_node):
        self.node_count += 1
        print('\t' * self.tab_count, "New Block => ")
        self.inc_tab_count()
        for st in block_node.stmts:
            st.accept(self)
        self.dec_tab_count()

                
#Create a print visitor instance
print_visitor = PrintNodesVisitor()
