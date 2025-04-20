#First some AST Node classes we'll use to build the AST with
class ASTNode:
    def __init__(self):
        self.name = "ASTNode"    
class ASTProgramNode(ASTNode):
    def __init__(self):
        self.name = "ASTProgramNode"

class ASTStatementNode(ASTNode):
    def __init__(self):
        self.name = "ASTStatementNode"

class ASTExpressionNode(ASTNode):
    def __init__(self):
        self.name = "ASTExpressionNode"

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
    def __init__(self, lexeme):
        self.name = "ASTFactorNode"
        self.lexeme = lexeme
    
    def accept(self, visitor):
        visitor.visit_factor_node(self)

class ASTSimpleExpNode(ASTExpressionNode):
    def __init__(self, lhs, adop=None, rhs=None):
        self.name = "ASTAdopNode"
        self.adop = adop
        self.left = lhs 
        self.right = rhs
    
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
    def __init__(self, expr):
        self.name = "ASTReturnNode"
        self.expr = expr
        self.type = None
    
    def accept(self, visitor):
        visitor.visit_return_node(self)

class ASTIfNode(ASTNode):
    def __init__(self, conds, block, elseBlock = None):
        self.name = "ASTIfNode"
        self.params = conds
        self.block = block
        self.elseBlock = elseBlock
    
    def accept():
        pass


class ASTTermNode(ASTExpressionNode):
    def __init__(self, lhs, mulop=None, rhs=None):
        self.name = "ASTTermNode"
        self.mulop = mulop
        self.left = lhs 
        self.right = rhs
    
    def accept(self, visitor):
        visitor.visit_term_node(self)

class ASTIntegerNode(ASTExpressionNode):
    def __init__(self, v):
        self.name = "ASTIntegerNode"
        self.value = v

    def accept(self, visitor):
        visitor.visit_integer_node(self)   

class ASTColourNode(ASTExpressionNode):
    def __init__(self, colour):
        self.name = "ASTColourNode"
        self.colour = colour

    def accept(self, visitor):
        visitor.visit_colour_node(self)

class ASTFloatNode(ASTExpressionNode):
    def __init__(self,v):
        self.name = 'ASTFloatNode'
        self.value = v   
    
    def accept(self, visitor):
        visitor.visit_float_node(self)

class ASTBoolNode(ASTExpressionNode):
    def __init__(self, v : bool):
        self.name = "ASTBoolNode"
        self.value = v

    def accept(self, visitor):
        visitor.visit_bool_node(self)

class ASTStringNode(ASTExpressionNode):
    def __init__ (self, string):
        self.name = "ASTStringNode"
        self.string = string 
    
    def accept(self, visitor):
        visitor.visit_string_node(self)
 
class ASTAssignmentNode(ASTStatementNode):
    def __init__(self, ast_var_node, ast_expression_node):
        self.name = "ASTStatementNode"        
        self.id   = ast_var_node
        self.expr = ast_expression_node

    def accept(self, visitor):
        visitor.visit_assignment_node(self)                

class ASTActualParamsNode(ASTNode):
    def __init__(self):
        self.name = 'ASTActualParamsNode'
        self.params = []

    def add_params(self, param):
        self.params.append(param)
    
    def accept(self, visitor):  
        visitor.visit_actual_params_node(self)
        
class ASTFunctionNode(ASTNode):
    def __init__(self):
        self.name = "ASTFunctionNode"
        self.params = []
        self.returnType = None
        self.block : ASTBlockNode = None

    def accept_params(self, visitor):
        for x in self.params:
            x.accept(visitor)

    def accept(self, visitor):
        visitor.visit_func_node(self)

class ASTIfNode(ASTNode):
    def __init__(self):
        self.name = "ASTFunctionNode"
        self.params = []
        self.returnType = None
        self.block : ASTBlockNode = None

    def accept_params(self, visitor):
        for x in self.params:
            x.accept(visitor)

    def accept(self, visitor):
        visitor.visit_func_node(self)

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
    
    def visit_actualparams_node(self,node):
        raise NotImplementedError()
    
    def visit_unary_node(self, node):
        raise NotImplementedError()
    
    def visit_factor_node(self, node):
        raise NotImplementedError()
    
    def visit_func_node(self, node):
        raise NotImplementedError()
    
    def visit_exp_node(self, node):
        raise NotImplementedError()
    
    def visit_string_node(self, node):
        raise NotImplementedError()
    
    def visit_colour_node(self, node):
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

class PrintNodesVisitor(ASTVisitor):
    def __init__(self):
        self.name = "Print Tree Visitor"
        self.node_count = 0
        self.tab_count = 0

    def inc_tab_count(self):
        self.tab_count += 1

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
        print('\t' * self.tab_count, "Parameters:: ", func_node.params)
        print('\t' * self.tab_count, "Return Type:: ", func_node.returnType)
        self.visit_block_node(func_node.block)

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
        node.expr.accept(self)
        self.dec_tab_count()

    def visit_if_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "If node ")
        print('\t' * self.tab_count, "Condition:: " , node.conds.accept() )
        self.inc_tab_count()
        print('\t' * self.tab_count, "Block:: " , node.block.accept())
        print('\t' * self.tab_count, "Else:: " , node.elseBlock.accept())
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
        print('\t' * self.tab_count, "Expression Node:")
        print('\t' * self.tab_count, "of Type : ", node.type)
        if node and node.left and node.right:
            print('\t' * self.tab_count, "Expression Operator => ", node.op)
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

#assume root node the AST assignment node .... 
#x=23



# print("Building AST for assigment statement x=23;")
# assignment_lhs = ASTVariableNode("x")
# assignment_rhs = ASTIntegerNode(23)
# root = ASTAssignmentNode(assignment_lhs, assignment_rhs)
# root.accept(print_visitor)
# print("Node Count => ", print_visitor.node_count)
# print("----")
# #assume root node the AST variable node .... 
# #x123 
# print("Building AST for variable x123;")
# root = ASTVariableNode("x123")
# root.accept(print_visitor)
# print("Node Count => ", print_visitor.node_count)