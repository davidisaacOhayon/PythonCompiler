
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
        self.tokenTypes = [lex.TokenType.Integer, lex.TokenType.FloatLiteral, lex.TokenType.BooleanLiteral, lex.TokenType.ColourLiteral, lex.TokenType.Identifier,lex.TokenType.PadRandI, lex.TokenType.PadHeight, lex.TokenType.PadWidth, lex.TokenType.PadRead]
        self.commands = [lex.TokenType.WriteBox, lex.TokenType.Print, lex.TokenType.Write]
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
 
        self.PreviousTokenSkipWS()
 
        while (self.crtToken.type == lex.TokenType.Whitespace):
            self.PreviousTokenSkipWS()
 
    def ReturnASTNode(self):

        # This function technically serves as to return a Factor.

        match self.crtToken.type:
            case lex.TokenType.Integer: return ast.ASTIntegerNode(self.crtToken.lexeme)
            case lex.TokenType.FloatLiteral : return ast.ASTFloatNode(self.crtToken.lexeme)
            case lex.TokenType.ColourLiteral : return ast.ASTColourNode(self.crtToken.lexeme)
            case lex.TokenType.BooleanLiteral : return ast.ASTBoolNode(self.crtToken.lexeme)
            case lex.TokenType.String : return ast.ASTStringNode(self.crtToken.lexeme)
            case lex.TokenType.Identifier : return ast.ASTVariableNode(self.crtToken.lexeme)
            case lex.TokenType.PadWidth : return ast.ASTWidthNode()
            case lex.TokenType.PadHeight : return ast.ASTHeightNode()
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


            if (self.crtToken.type == lex.TokenType.Relop):
                return ast.ASTTermNode(tempLeft, oper, tempRight)
 
            
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
        # Parse Expression until ; or ) or } is hit
        while self.crtToken.type not in [lex.TokenType.End, lex.TokenType.Parameter_R, lex.TokenType.Declaration_R]:
            if (self.crtToken.type in self.tokenTypes):
                if tempLeft is None:
                    tempLeft = self.ReturnASTNode()
                else:
                    tempRight = self.ReturnASTNode()
                self.NextToken()


            if (self.crtToken.type == lex.TokenType.Relop):
                return ast.ASTSimpleExpNode(tempLeft, oper, tempRight)

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
 
                    tempRight = self.ParseTerm()


        
        return ast.ASTSimpleExpNode(tempLeft, oper, tempRight)

 
    def ParseExpression(self):
        # Expressions defined as Left <Relop> Right

        left = None

        if self.crtToken.type in self.tokenTypes:
            # Assign lhs
            left = self.ReturnASTNode()
            
            self.NextToken()

 
        while self.crtToken.type != lex.TokenType.End and self.crtToken.type != lex.TokenType.Parameter_R:
 
            # For N <Relop> N expressions
            if self.crtToken.type == lex.TokenType.Relop:
                # Get operator
                op = self.crtToken.lexeme
                self.NextToken()
                # Initiate Rhs for exp
                tempRight = None
                if self.crtToken.type in self.tokenTypes:
                    tempRight = self.ReturnASTNode()

                    self.NextToken()

                    # Case Where N <Op> m <Op> P ....
                    if self.crtToken.type in [lex.TokenType.Addop, lex.TokenType.Mulop, lex.TokenType.Relop]:
                        self.PreviousToken()
                        tempRight = self.ParseExpression()

                    # Case where N and M
                    if self.crtToken.type == lex.TokenType.And:
                        # Declare preceding Expression N
                        tempLeft = ast.ASTExpNode(left, None, op, tempRight)
                        # Get AND operator
                        oper = self.crtToken.lexeme
                        # Jump next token
                        self.NextToken()
                        # Parse new Right expression M
                        tempRight = self.ParseExpression()
                        # Return resulting expression
                        return ast.ASTExpNode(tempLeft, None, oper, tempRight)
                    
                    # Case where N or M
                    if self.crtToken.type == lex.TokenType.Or:
                        # Declare preceding Expression N
                        tempLeft = ast.ASTExpNode(left, None, op, tempRight)
                        # Get AND operator
                        oper = self.crtToken.lexeme
                        # Jump next token
                        self.NextToken()
                        # Parse new Right expression M
                        tempRight = self.ParseExpression()
                        # Return resulting expression
                        return ast.ASTExpNode(tempLeft, None, oper, tempRight)
                        
            

                return ast.ASTExpNode(left, None, op, tempRight)

            if self.crtToken.type == lex.TokenType.And:
                op = self.crtToken.lexeme
                self.NextToken()
                right = self.ParseTerm()
                return ast.ASTExpNode(left, None, op, right)

            # For N <Addop> M expressions
            if self.crtToken.type == lex.TokenType.Addop:
                self.PreviousToken()
                left = self.ParseSimpleExpression()

            # For N <Mulop> M expressions
            if self.crtToken.type == lex.TokenType.Mulop:
                self.PreviousToken()
                left = self.ParseTerm()

        return left

    def ParseParameters(self):
        tType = None
        tName = None
        param = None

        if (self.crtToken.type == lex.TokenType.Identifier):
            tName = self.crtToken.lexeme 
            self.NextToken()
            if (self.crtToken.type == lex.TokenType.Colon):
                self.NextToken()
                tType = self.GetIdentType()
                param = ast.ASTFormalParamNode(tName, tType)
                self.NextToken()
        return param

    def ParseFunction(self):
        if (self.crtToken.type == lex.TokenType.Function):
            tempFunc = ast.ASTFunctionNode()

            # Skip whitespacesto get func name 
            self.NextToken()
            if (self.crtToken.type == lex.TokenType.FunctionCall):
                tempFunc.name = self.crtToken.lexeme.replace('(', '')
            # Get Parameters

            # if (self.crtToken.type == lex.TokenType.Parameter_L):
            while(self.crtToken.type != lex.TokenType.Parameter_R):
                self.NextToken()
                print(self.crtToken.lexeme)
                params = self.ParseParameters()
                tempFunc.params.add_params(params)
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
   
    def ParseFunctionCall(self):
        if self.crtToken.type == lex.TokenType.FunctionCall:
            # Remove brackets to retrieve name
            funcName = self.crtToken.lexeme.replace('(', '')
            tempFuncCall = ast.ASTFunctionCall()
            tempFuncCall.name = funcName
            tempParams = []
            
        while(self.crtToken.type != lex.TokenType.Parameter_R):
            self.NextToken()
            param = self.ParseExpression()
            tempParams.append(param)
            if (self.crtToken.type == lex.TokenType.Parameter_R):
                tempFuncCall.params = tempParams
        return tempFuncCall
       
    def ParseWriteBox(self):
        print(self.crtToken.lexeme)
        args = {}
        arg = 0
        arg5 = None
        while (self.crtToken.type != lex.TokenType.End):
  
            if self.crtToken.type == lex.TokenType.WriteBox:
                self.NextToken()
                print(self.crtToken.lexeme)
                continue

            elif (self.crtToken.type == lex.TokenType.Comma):
                self.NextToken()
                continue

            elif self.crtToken.type == lex.TokenType.Identifier:
                arg += 1
                args[arg] = self.crtToken.lexeme
                self.NextToken()
 
                continue

            elif self.crtToken.type == lex.TokenType.Integer:
                arg += 1
                args[arg] = self.crtToken.lexeme
                self.NextToken()
 
                continue

            elif self.crtToken.type == lex.TokenType.ColourLiteral:
                arg5 = self.crtToken.lexeme
                self.NextToken()
                print(self.crtToken.lexeme)
                continue
            else:
                raise SyntaxError("Invalid arguments for Write Box")

                    
        if not arg5:
            raise SyntaxError("Invalid argument for color in writebox")

        return ast.ASTWriteBoxNode(args[1], args[2], args[3], args[4], arg5)
        
    def ParseWrite(self):
        print(self.crtToken.lexeme)
        args = {}
        arg = 0
        arg4 = None
        while (self.crtToken.type != lex.TokenType.End):
            print(self.crtToken.lexeme)    
            if self.crtToken.type == lex.TokenType.Write:
                self.NextToken()
                print(self.crtToken.lexeme)
                continue

            elif (self.crtToken.type == lex.TokenType.Comma):
                self.NextToken()
                continue

            elif self.crtToken.type == lex.TokenType.Identifier:
                arg += 1
                args[arg] = self.crtToken.lexeme
                self.NextToken()
 
                continue

            elif self.crtToken.type == lex.TokenType.Integer:
                arg += 1
                args[arg] = self.crtToken.lexeme
                self.NextToken()
 
                continue

            elif self.crtToken.type == lex.TokenType.ColourLiteral:
                arg4 = self.crtToken.lexeme
                self.NextToken()
                print(self.crtToken.lexeme)
                continue
            else:
                print(self.crtToken.lexeme)
                raise SyntaxError("Invalid arguments for write statement.")

                    
        if not arg4:
            raise SyntaxError("Invalid argument for color in write statement.")

        return ast.ASTWriteNode(args[1], args[2], arg4)

    def ParseIf(self):
        
        block = conds = nxtBlock = None

        self.NextToken()
        if self.crtToken.type == lex.TokenType.Parameter_L:
            self.NextToken()
            conds = self.ParseExpression()
        
        print(self.crtToken.lexeme)
        if self.crtToken.type == lex.TokenType.Parameter_R:
            print('changed 1 : ', self.crtToken.lexeme)
            self.NextToken()
            print('changed 2 : ', self.crtToken.lexeme)
            self.NextToken()
            print('changed 3 : ', self.crtToken.lexeme)
            block = self.ParseBlock()
            self.NextToken()
            

        if self.crtToken.lexeme == "else":
            print('else found')
            self.NextToken()
            self.NextToken()
            print(self.crtToken.lexeme)
            nxtBlock = self.ParseBlock()
        
        return ast.ASTIfNode(conds,block,nxtBlock)
    
    def ParseFor(self):
        if self.crtToken.lexeme == "for":
            self.NextToken()
        
        if self.crtToken.type == lex.TokenType.Parameter_L:
            # Skip let
            self.NextToken()
            self.NextToken()
            # Parse Assignment Part
            assign = self.ParseAssignment()
            self.NextToken()
            # Parse Condition Part
            cond = self.ParseExpression()
            self.NextToken()
            # Parse Step Part
            step = self.ParseAssignment()
            self.NextToken()
            self.NextToken()
            block = self.ParseBlock()


            return ast.ASTForNode(assign, cond, step, block)

    def ParseWhile(self):
        if self.crtToken.lexeme == "while":
            self.NextToken()
 
        if self.crtToken.type != lex.TokenType.Parameter_L:
            raise SyntaxError("Missing Bracket")
        
        self.NextToken()
        expr = self.ParseExpression()
        
        if self.crtToken.type != lex.TokenType.Parameter_R:
            raise SyntaxError("Missing Bracket")
        
        self.NextToken()
        self.NextToken()
        block = self.ParseBlock()

        return ast.ASTWhileNode(expr, block)

    def ParseKeyword(self):
        if self.crtToken.lexeme == "return":
            self.NextToken()
            type = self.crtToken.type
            
            return ast.ASTReturnNode(self.ParseExpression(), type) 
    
        elif self.crtToken.lexeme == "if":
            return self.ParseIf()
        
        elif self.crtToken.lexeme == "for":
            return self.ParseFor()
        
        elif self.crtToken.lexeme == "while":
            return self.ParseWhile()
        
        elif self.crtToken.lexeme == "let":
            return self.ParseAssignment()

# Used for redeclaring values of variables 
    def ParseReassignment(self):
        if self.crtToken.type == lex.TokenType.Identifier:
            assignment_lhs = ast.ASTVariableNode(self.crtToken.lexeme)
            self.NextToken()

        if (self.crtToken.type == lex.TokenType.AssignOp):
            self.NextToken()
            tempRhs = self.ParseExpression()
            assignment_rhs = ast.ASTExpNode(tempRhs, tempRhs.type)

            return ast.ASTReAssignNode(assignment_lhs, assignment_rhs)
        else:
            raise SyntaxError("Invalid Statement")

    def ParseAssignment(self):  
        expType = None
        if (self.crtToken.lexeme == "let"):
            self.NextToken()

        #Assignment is made up of two main parts; the LHS (the variable) and RHS (the expression)
        if (self.crtToken.type == lex.TokenType.Identifier):
            #create AST node to store the identifier            
            assignment_lhs = ast.ASTVariableNode(self.crtToken.lexeme)
            self.NextToken()
            # Check if statement is in the form x = expr (reassignment)
            if (self.crtToken.type == lex.TokenType.AssignOp):
                self.PreviousToken()
                assignment_rhs = self.ParseReassignment()
                return assignment_rhs

        if (self.crtToken.type == lex.TokenType.Colon):

            self.NextToken()
            
            expType = self.GetIdentType()
            
            self.NextToken()
             
        if (self.crtToken.type == lex.TokenType.AssignOp):
 
            self.NextToken()
 
            #Next sequence of tokens should make up an expression ... therefor call ParseExpression that will return the subtree representing that expression
            tempRhs = self.ParseExpression()

            assignment_rhs = ast.ASTExpNode(tempRhs, expType)

            return ast.ASTAssignmentNode(assignment_lhs, assignment_rhs)
 
        # If Token meets an end, this is a declaration. (i.e. x:int;)
        elif (self.crtToken.type == lex.TokenType.End or self.crtToken.type == lex.TokenType.Comma or self.crtToken.type == lex.TokenType.Parameter_R):
          
          return ast.ASTDeclareNode(assignment_lhs, expType)

    def ParseStatement(self):
        print(self.crtToken.lexeme)
        #At the moment we only have assignment statements .... you'll need to add more for the assignment - branching depends on the token type
        if self.crtToken.type == lex.TokenType.Identifier:
            return self.ParseAssignment()
        
        elif self.crtToken.type == lex.TokenType.Function:
            return self.ParseFunction()
        
        elif self.crtToken.type == lex.TokenType.FunctionCall:
            return self.ParseFunctionCall()
        
        elif self.crtToken.type == lex.TokenType.Keyword:
            return self.ParseKeyword()
        
        elif self.crtToken.type == lex.TokenType.WriteBox:
            return self.ParseWriteBox()
        
        elif self.crtToken.type == lex.TokenType.Write:
            return self.ParseWrite()
        
        print(self.crtToken.lexeme)
        raise SyntaxError("Invalid Statement")
        
    def ParseBlock(self):
        #At the moment we only have assignment statements .... you'll need to add more for the assignment - branching depends on the token type
        block = ast.ASTBlockNode()

        # Process block before } or ;
        while (self.crtToken.type != lex.TokenType.End and self.crtToken.type != lex.TokenType.Parameter_R and self.crtToken.type != lex.TokenType.Declaration_R):
            s = self.ParseStatement()
            block.add_statement(s)
            if (self.crtToken.type == lex.TokenType.End):
                self.NextToken()
                # If next token is still END 
                if (self.crtToken.type == lex.TokenType.End):
                    return block
 

        return block

    def ParseProgram(self):                        
        self.NextToken()  #set crtToken to the first token (skip all WS)
        b = self.ParseBlock()        
        return ast.ASTProgramNode(b)       

    def Parse(self):        
        self.ASTroot = self.ParseProgram()



if __name__ == '__main__':

    inputCode = ""
    with open('./something.txt', 'r') as file:
     inputCode = file.read()

    parser = Parser("""
                    if ( 5 > 2  or 2 < 3) { return 5;}; 
                    """)
    parser.Parse()

    print_visitor = ast.PrintNodesVisitor()
    parser.ASTroot.accept(print_visitor)

 