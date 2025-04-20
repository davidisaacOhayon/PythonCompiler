import Lexer
import ASTNodes







# Now we need the parser (using tokens produced by the Lexer) to build the AST - this code snipper is able to build ASTAssignmentNode trees. LHS can only be an integer here ....
# A small predictive recursive descent parser
import ASTNodes as ast
import Lexer as lex

class Parser:
    def __init__(self, src_program_str):
        self.name = "PARSEAR"
        self.lexer = lex.Lexer(src_program_str)
        self.index = -1  #start at -1 so that the first token is at index 0
        self.src_program = src_program_str
        self.tokens = self.lexer.tokens
        self.tokenTypes = [lex.TokenType.Integer, lex.TokenType.FloatLiteral, lex.TokenType.BooleanLiteral, lex.TokenType.ColourLiteral, lex.TokenType.Identifier]
        print("[Parser] Lexer generated token list ::")
        for t in self.tokens:
           print(t.type, t.lexeme)
        self.crtToken = lex.Token("", lex.TokenType.Error)
        self.nextToken = lex.Token("", lex.TokenType.Error)
        self.ASTroot = ast.ASTAssignmentNode     #this will need to change once you introduce the AST program node .... that should become the new root node    

    def NextTokenSkipWS(self):
        self.index += 1   #Grab the next token
        if (self.index < len(self.tokens)):
            self.crtToken = self.tokens[self.index]
        else:
            self.crtToken = lex.Token(lex.TokenType.End, "END")

    def NextToken(self):
        self.NextTokenSkipWS()
        while (self.crtToken.type == lex.TokenType.Whitespace):
            self.NextTokenSkipWS()

    def GetIdentType(self):
            match self.crtToken.type:
                case lex.TokenType.IntegerType: return "Int"
                case lex.TokenType.FloatType: return "Float"
                case lex.TokenType.StringType: return "String"
                case lex.TokenType.BoolType: return "Boolean"
                case lex.TokenType.ColourType: return "Colour"
                case _: raise Exception("Syntax Error, Invalid Type.")

    def PreviousTokenSkipWS(self):
        self.index -= 1   #Grab the Previous token
        if (self.index < len(self.tokens) and self.index > -1):
            self.crtToken = self.tokens[self.index]
        else:
            self.crtToken = lex.Token(lex.TokenType.End, "END")

    def PreviousToken(self):
        print('Current Token before previous', self.crtToken.lexeme, ' Index', self.index)
        print('current Index', self.index)
        self.PreviousTokenSkipWS()
        print('current Index', self.index)
        print('Gone back to ', self.crtToken.lexeme)
        while (self.crtToken.type == lex.TokenType.Whitespace):
            self.PreviousTokenSkipWS()
            print('current Index', self.index)
            print('Gone back to ', self.crtToken.lexeme)

    def ReturnASTNode(self):
        match self.crtToken.type:
            case lex.TokenType.Integer: return ast.ASTIntegerNode(self.crtToken.lexeme)
            case lex.TokenType.FloatLiteral : return ast.ASTFloatNode(self.crtToken.lexeme)
            case lex.TokenType.ColourLiteral : return ast.ASTColourNode(self.crtToken.lexeme)
            case lex.TokenType.BooleanLiteral : return ast.ASTBoolNode(self.crtToken.lexeme)
            case lex.TokenType.String : return ast.ASTStringNode(self.crtToken.lexeme)
            case lex.TokenType.Identifier : return ast.ASTVariableNode(self.crtToken.lexeme)
            case _:
                return 

    def ParseTerm(self):
        tempLeft = tempRight = oper = None
        while self.crtToken.type != lex.TokenType.End:

            if self.crtToken.type in self.tokenTypes:
                if tempLeft:
                    tempRight = self.ReturnASTNode()
                    self.NextToken()
                else:
                    tempLeft = self.ReturnASTNode()
                    self.NextToken()
            
            if self.crtToken.type == lex.TokenType.Addop:
                self.PreviousToken()
                tempRight = self.ParseSimpleExpression()

            if (self.crtToken.type == lex.TokenType.Mulop):
                if oper is None:
                    oper = self.crtToken.lexeme
                    self.NextToken()
                else:
                    self.PreviousToken()
                    tempRight = self.ParseTerm()
        
        print(f'Creating Term Node with {tempLeft}, {oper} and {tempRight}')
        return ast.ASTTermNode(tempLeft, oper, tempRight)

    def ParseSimpleExpression(self):
        tempLeft = tempRight = oper = None
        # Parse Expression until semi colon is hit
        while self.crtToken.type != lex.TokenType.End:

            if (self.crtToken.type in self.tokenTypes):
                if tempLeft is None:
                    tempLeft = self.ReturnASTNode()
                else:
                    tempRight = self.ReturnASTNode()
                self.NextToken()

            if (self.crtToken.type == lex.TokenType.Addop):
                # Check if preceding operator exists
                if oper is None:
                   oper = self.crtToken.lexeme
                   self.NextToken()
                # if exists, parse a nested simple expression e.g. 2 + (3 + 4)
                else:
                    self.PreviousToken()
                    tempRight = self.ParseSimpleExpression()
            
            if (self.crtToken.type == lex.TokenType.Mulop):
                if oper is None:
                    oper = self.crtToken.lexeme
                    self.NextToken()
                else:
                    self.PreviousToken()
                    print(f'Left {tempLeft}, Operator {oper}, Right {tempRight}')
                    tempRight = self.ParseTerm()


        
        return ast.ASTSimpleExpNode(tempLeft, oper, tempRight)
                          
    def ParseExpression(self):
        left = None
        if self.crtToken.type in self.tokenTypes:
            left = self.ReturnASTNode()
            self.NextToken()

        # For N (Relop) N expressions
        if self.crtToken.type == lex.TokenType.Relop:
            op = self.crtToken.lexeme
            self.NextToken()
            tempRight = None
            if self.crtToken.type in self.tokenTypes:
                tempRight = self.ReturnASTNode()
                self.NextToken()
                if self.crtToken.type in [lex.TokenType.Addop, lex.TokenType.Mulop, lex.TokenType.Relop]:
                    self.PreviousToken()
                    tempRight = self.ParseExpression()
        
            # NOTE : This is a simple implementation of the above logic, EXPRESSIONS FOR NOW ARE ONLY TEMPORARILY ASSIGNED OF TYPE NONE, FIX ASAP.
            return ast.ASTExpNode(left, None, op, tempRight)

            
        # For N (Addop) N expressions
        if self.crtToken.type == lex.TokenType.Addop:
            self.PreviousToken()
            left = self.ParseSimpleExpression()

        # For N (Mulop) N expressions
        if self.crtToken.type == lex.TokenType.Mulop:
            self.PreviousToken()
            left = self.ParseTerm()

        return left

    def ParseParameters(self):
        params = []
        tType = None
        tName = None
        if (self.crtToken.type == lex.TokenType.Identifier):
            tName = self.crtToken.lexeme 
            self.NextToken()
            if (self.crtToken.type == lex.TokenType.Colon):
                self.NextToken()
                tType = self.GetIdentType()
                params.append((tName, tType))
                self.NextToken()
        return params

    def ParseFunction(self):
        if (self.crtToken.type == lex.TokenType.Function):
            tempFunc = ast.ASTFunctionNode()

            # Skip whitespacesto get func name 
            self.NextToken()
            if (self.crtToken.type == lex.TokenType.Identifier):
                tempFunc.name = self.crtToken.lexeme
            # Get Parameters
            self.NextToken()
            if (self.crtToken.type == lex.TokenType.Parameter_L):
                while(self.crtToken.type != lex.TokenType.Parameter_R):
                    self.NextToken()
                    params = self.ParseParameters()
                    tempFunc.params.extend(params)
                self.NextToken()

            if (self.crtToken.type == lex.TokenType.CastOp):
                self.NextToken()
                tempFunc.returnType = self.GetIdentType()
                self.NextToken()
            
            if (self.crtToken.type == lex.TokenType.Declaration_L):
                    print(self.crtToken.lexeme)
                    self.NextToken()
                    print(self.crtToken.lexeme)
                    tempFunc.block  = self.ParseBlock()
                
            
        return tempFunc
    
    def ParseIf(self):
        conds = []
        block = nxtBlock = None
        self.NextToken()
        if self.crtToken.type == lex.TokenType.Parameter_L:
            self.NextToken()
            conds.append(self.ParseExpression())
        
        if self.crtToken.type == lex.TokenType.Parameter_R:
            self.NextToken()
            block = self.ParseBlock()

        if self.crtToken.lexeme == "else":
            self.NextToken()
            nxtBlock = self.ParseBlock()
        
        return ast.ASTIfNode(conds,block,nxtBlock)

        

        

    def ParseKeyword(self):
        if self.crtToken.lexeme == "return":
            self.NextToken()
            return ast.ASTReturnNode(self.ParseExpression()) 
        
        elif self.crtToken.lexeme == "if":
            return self.ParseIf()
            
            

    def ParseAssignment(self):
        expType = None

        #Assignment is made up of two main parts; the LHS (the variable) and RHS (the expression)
        if (self.crtToken.type == lex.TokenType.Identifier):
            #create AST node to store the identifier            
            assignment_lhs = ast.ASTVariableNode(self.crtToken.lexeme)

            self.NextToken()
            #print("Variable Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)
        if (self.crtToken.type == lex.TokenType.Colon):

            self.NextToken()
            
            expType = self.GetIdentType()
            
            print(self.crtToken.lexeme)
            
            self.NextToken()

        if (self.crtToken.type == lex.TokenType.Relop):
            self.PreviousToken()
            return ast.ASTExpNode()
        
        if (self.crtToken.type == lex.TokenType.AssignOp):
            self.NextToken()
            #Next sequence of tokens should make up an expression ... therefor call ParseExpression that will return the subtree representing that expression
            tempRhs = self.ParseExpression()

            assignment_rhs = ast.ASTExpNode(tempRhs, expType)

            if assignment_rhs:
                return ast.ASTAssignmentNode(assignment_lhs, assignment_rhs)
            #print("EQ Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)

        # If Token meets an end, this is a declaration. (i.e. x:int;)
        elif (self.crtToken.type == lex.TokenType.End or self.crtToken.type == lex.TokenType.Comma or self.crtToken.type == lex.TokenType.Parameter_R):
          return ast.ASTDeclareNode(assignment_lhs, expType)



            
    def ParseStatement(self):
        #At the moment we only have assignment statements .... you'll need to add more for the assignment - branching depends on the token type
        if self.crtToken.type == lex.TokenType.Identifier:
            return self.ParseAssignment()
        
        elif self.crtToken.type == lex.TokenType.Function:
            return self.ParseFunction()
        
        elif self.crtToken.type == lex.TokenType.Keyword:
            return self.ParseKeyword()
        
    def ParseBlock(self):
        #At the moment we only have assignment statements .... you'll need to add more for the assignment - branching depends on the token type
        block = ast.ASTBlockNode()

        while (self.crtToken.type != lex.TokenType.End and self.crtToken.type != lex.TokenType.Parameter_R):
            #print("New Statement - Processing Initial Token:: ", self.crtToken.type, self.crtToken.lexeme)
            s = self.ParseStatement()
            block.add_statement(s)
            if (self.crtToken.type == lex.TokenType.End):
                self.NextToken()
                print(f'Here we go{self.crtToken.lexeme}')
            else:
                print("Syntax Error - No Semicolon separating statements in block")
                break
        
        return block

    def ParseProgram(self):                        
        self.NextToken()  #set crtToken to the first token (skip all WS)
        b = self.ParseBlock()        
        return b        

    def Parse(self):        
        self.ASTroot = self.ParseProgram()



if __name__ == '__main__':
    inputCode = ""
    with open('./something.txt', 'r') as file:
        inputCode = file.read()
 
    parser = Parser('x:int = 5 + 5 * y;')
    parser.Parse()

    print_visitor = ast.PrintNodesVisitor()
    parser.ASTroot.accept(print_visitor)

 