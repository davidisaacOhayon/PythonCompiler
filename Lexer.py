import re 
from enum import Enum

class TokenType(Enum):
    Identifier = 1
    Integer = 2
    String = 3
    Char = 4
    FloatLiteral = 5
    Comment = 6
    Whitespace = 7
    Operator = 8
    SemiColon = 9
    Colon = 10
    Comma = 11
    Keyword = 12
    End = 13
    CastOp = 14
    AssignOp = 15
    Error = 16
    BooleanLiteral = 17
    Mulop = 18
    Addop = 19
    Declaration_L= 20
    Declaration_R = 21
    Parameter_L = 22
    Parameter_R = 23
    Array_L = 24
    Array_R = 25
    Function = 26
    Relation = 27
    Unary = 28
    ColourLiteral = 29
    Relop = 47


    # Token Typing for Identifiers
    IntegerType = 30
    FloatType = 31
    CharType = 32
    StringType = 33
    ColourType = 34
    BoolType = 35

    # Token typing for Width, Height, Read , RandI, Print, Delay & Write
    PadWidth = 36
    PadHeight = 37
    PadRead = 38
    PadRandI = 39 
    Print = 40
    Delay = 41
    WriteBox = 42
    Write = 43 

    FunctionCall = 44

    And = 45
    Or = 46





Keywords = {'for', 'while', 'if', 'else', 'return', 'let'}
Types = {'int' : TokenType.IntegerType, 'float' : TokenType.FloatType, 'char' : TokenType.CharType, 'string' : TokenType.StringType, 'bool' : TokenType.BoolType, 'colour' : TokenType.ColourType}
Returns = {'void'}.update(Types)
RelationOp = {'!','<', '>', "==", "!=", "<=", ">="}
AddOp = {"+", "-", 'or'}
MulOp = {"*","/", "and"}
AssignOp = {'='}
SemiColon = {';'}
Colon = {':'}
Comma = {','}
# For functions, dictionaries
Declaration_L = {'{'}
Declaration_R = {'}'}
# For Paranthesis
Parameter_L = {'('}
Parameter_R = {')'}
# For Arrays
Array_L = {'['}
Array_R = {']'}
Function = {'fun'}
Booleans = {'true', 'false'}
cast_operators = {'->'}


class Token():
    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme
    def __str__(self):
        return f"Token: {self.type} Lexeme: {self.lexeme}"



class Lexer():
    '''Implements Lexer Object'''
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_token_index = 0
        self.position = 0

        self.__initTables()
        self.__tokenize()
        print("\n")
        print("\n")
        print(self.tokens[0])

    def __initTables(self):
        ''' Initializes transition tabes and accept states for lexer'''
        self.states = {
            # Start
            0 : {'letter' : 1, 
                 'digit' : 2,
                 'comment' : 3, 
                 "whitespace" : 4,
                 "other" : -1, 
                 "_" : 1, 
                 "semicolon" : 6, 
                 'assign_op' : 7, 
                 'addop': 8, 
                 'mulop': 9, 
                 'operator': 5,
                 'array_L': 11,
                 'array_R': 12,
                 'parameter_L' : 13,
                 'parameter_R' : 14,
                 'declare_L' : 15,
                 'declare_R' : 16,
                 'colon' : 17,
                 'comma' : 18,
                 'function' : 19,
                 'relation' : 20,
                 '#' : 21,
                 ',' : 22,
                 ':' : 23,
                 'relop' : 24,
                 'funCall' : 25
            },
            # String
            1 : {'letter' : 1, 'digit' : 1, '_' : 1},
            # Digit
            2 : {'digit' : 2, "." : 10},
            # Comment
            3 : {'comment' : 3, 'letter' : 3, 'digit': 3, 'whitespace' : 3, 'other' : 3, 'separator' : 3},
            # Whitespace
            4 : {'whitespace' : 4}, # -1
            # Operator
            5 : {'operator' : 5}, # -1
            # Separator
            6 : {'semicolon' : 6}, # -1
            # Assign Op (=)
            7 : {'assign_op' : 24, 'operator': 7}, # -1
            # Add Op (+, -)
            8 : {'addop' : 8 },
            # Mul Op (*, /)
            9 : {'mulop' : 10},
            # Array []
            11 : {'array_L' : 11},
            12 : {'array_R' : 12},
            # Parameter ()
            13: {'parameter_L' : 13},
            14 : {'parameter_R' : 14},
            # Declare {}
            15 : {'declare_L' : 15},
            16 : {'declare_R' : 16},
            17 : {'colon' : 17},
            18 : {'comma' : 18},
            19 : {'function' : 19},
            20 : {'relation' : 20},
            21 : {'#' : 21, 'digit' : 21, 'letter' : 21},
            22 : {',' : 22},
            23 : {':' : 23},
            24 : {'relop' : 24, 'assign_op' : 24},  
            


            # Exclusive States
            # Float
            10 : {'digit' : 10},
        }


        self.accepts = {
            1 : TokenType.Identifier,
            2 : TokenType.Integer,
            3 : TokenType.Comment,
            4 : TokenType.Whitespace,
            5 : TokenType.Operator,
            6 : TokenType.End,
            7 : TokenType.AssignOp,
            8 : TokenType.Addop,
            9 : TokenType.Mulop,
            10 : TokenType.FloatLiteral,
            11 : TokenType.Array_L,
            12 : TokenType.Array_R,
            13 : TokenType.Parameter_L,
            14 : TokenType.Parameter_R,
            15 : TokenType.Declaration_L,
            16 : TokenType.Declaration_R,
            17 : TokenType.Colon,
            18 : TokenType.Comma,
            19 : TokenType.Function,
            20 : TokenType.Relation,
            21 : TokenType.ColourLiteral,
            22 : TokenType.Comma,
            23 : TokenType.Colon,
            24 : TokenType.Relop,
            25 : TokenType.FunctionCall
        }


    def __checkKeyword(self, lexeme):
        if lexeme in Keywords:
            return TokenType.Keyword, lexeme
        elif lexeme in Types.keys():
            return Types[lexeme], lexeme
        elif lexeme == 'or':
            return TokenType.Or, lexeme
        elif lexeme == 'and':
            return TokenType.And, lexeme
        elif lexeme in Booleans:
            return TokenType.BooleanLiteral, lexeme
        elif lexeme == 'fun':
            return TokenType.Function, lexeme
        elif lexeme == '__width':
            return TokenType.PadWidth, lexeme
        elif lexeme == '__height':
            return TokenType.PadHeight, lexeme
        elif lexeme == '__read':
            return TokenType.PadRead, lexeme
        elif lexeme == '__random_int':
            return TokenType.PadRandI, lexeme
        elif lexeme == '__write_box':
            return TokenType.WriteBox, lexeme
        elif lexeme == '__write':
            return TokenType.Write, lexeme
        elif lexeme == '__print':
            return TokenType.Print, lexeme



        
        else: return False
    
    def printTokens(self):
        for token in self.tokens:
            print(token)

    def __tokenize(self):
        '''Begin main process of tokenizing source code'''
        state = 0
        lexeme = ""

        while self.position < len(self.code):
                char = self.code[self.position]
                type = self.__getTokenCategory(char)
                print(f'state : {state} position : {self.position} char : {char} type : {type}')
                # try:

                # Handle Cast Operator case
                if (self.code[self.position:self.position+2] == '->'):
                    self.tokens.append(Token(TokenType.CastOp, '->'))
                    lexeme = ""
                    self.position += 2
                    continue

                if type in self.states[state]:
                    # go to next state
                    state = self.states[state][type]
                    self.position += 1 
                    lexeme += char
                else:
                    if lexeme:
                        if state in self.accepts:
                            if (self.__checkKeyword(lexeme)):
                                TokenType, lexeme = self.__checkKeyword(lexeme)
                                self.tokens.append(Token(TokenType, lexeme))
                            else:
                                 print()
                                 self.tokens.append(Token(self.accepts[state],lexeme))

                            state = 0
                            lexeme = ""
                    else:
                        state = 0
                        lexeme = ""

    def getNextToken(self):
        currentToken = self.tokens[self.current_token_index]
        self.current_token_index += 1
        return currentToken

    def __getTokenCategory(self, ch):
        cat = 'other' 
        if ch.isspace():
            cat = 'whitespace'
        if ch in ['_', ".", "#", ":"]:
            print('we have a colon')
            cat = ch
        elif ch in AddOp:
            cat = 'addop'
        elif ch in MulOp:
            cat = 'mulop'
        elif ch in SemiColon:
            cat = 'semicolon'
        elif ch in Colon:
            cat = 'colon'
        elif ch in Comma:
            cat = 'comma'
        elif ch in RelationOp:
            cat = 'relop'
        elif ch in AssignOp:
            cat = 'assign_op'
        elif ch in Declaration_R:
            cat = 'declare_R'
        elif ch in Declaration_L:
            cat = 'declare_L'
        elif ch in Parameter_R:
            cat = 'parameter_R'
        elif ch in Parameter_L:
            cat = 'parameter_L'
        elif ch in Array_L:
            cat = 'array_L'
        elif ch in Array_R:
            cat = 'array_R'
        elif re.search(r"[a-zA-Z]", ch):
            return 'letter'
        elif re.search(r"[0-9]", ch):
            return 'digit'
        return cat
        


if __name__ == '__main__':
    lex = Lexer(""" 
                    let c:int = test(2, 312);
                              
                    fun test(a:int, b:int) -> int{
                        let x : int = 5;  
                        if ( b > a ){
                              return b;
                        }

                        return a;
                    }
                    __print c;  
 
                    """)
    lex.printTokens()



 
 
 
