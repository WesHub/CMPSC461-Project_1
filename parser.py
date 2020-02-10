# authored by weslee hwang; all rights reserved; do not distribute

# project1: sql parser
#INT, FLOAT, ID, TERM, SEMICOLON, KEYWORD, ASSIGNMENTOP, OPERATOR, COMMA, EOI, INVALID = 1, 2, 3, 4, 5, 6, 7
INT, FLOAT, ID, KEYWORD, OPERATOR, COMMA, COND, CONDLIST, EOI, INVALID = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
import sys

def typeToString(tp):
    if (tp == INT):
        return "Int"
    elif (tp == FLOAT):
        return "Float"
    elif (tp == ID):
        return "Id"
    elif (tp == KEYWORD):
        return "Keyword"
    elif (tp == OPERATOR):
        return "Operator"
    elif (tp == COMMA):
        return "Comma"
    elif (tp == COND):
        return "Cond"
    elif (tp == CONDLIST):
        return "Condlist"
    elif (tp == EOI):
        return "EOI"
    return "Invalid"


class Token: #COMPLETE
    "A class for representing Tokens"

    # a Token object has two fields: the token's type and its value
    def __init__(self, tokenType, tokenVal):
        self.type = tokenType
        self.val = tokenVal

    def getTokenType(self):
        return self.type

    def getTokenValue(self):
        return self.val

    def __repr__(self):  # returns object representation
        if (self.type in [INT, FLOAT, ID, OPERATOR]):
            return self.val
        elif(self.type == KEYWORD):
            return self.val
        elif(self.type == COMMA):
            return ","
        elif (self.type == EOI):
            return ""
        else:
            return "invalid"


LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"


class Lexer:
    # COMPLETE
    # class for forming the grammar
    # stmt is the current statement to perform the lexing;
    # index is the index of the next char in the statement

    def __init__(self, s):  # Constructor Function
        self.stmt = s
        self.index = 0
        self.nextChar()

    def nextToken(self):
        while True:
            if self.ch.isalpha():  # is a keyword or a id
                id = self.consumeChars(LETTERS + DIGITS)
                if id == "SELECT" or id == "FROM" or id == "WHERE" or id == "AND":
                    return Token(KEYWORD, id)
                else:
                    return Token(ID, id)
            elif self.ch.isdigit():  # is a digit
                num = self.consumeChars(DIGITS)
                if self.ch != ".":  # is not a float
                    return Token(INT, num)
                num += self.ch
                self.nextChar()
                if self.ch.isdigit():  # decimal numbers
                    num += self.consumeChars(DIGITS)
                    return Token(FLOAT, num)
                else:
                    return Token(INVALID, num)  # no numbers afterwards
            elif self.ch == ' ':
                self.nextChar()
            elif self.ch == ',':
                self.nextChar()
                return Token(COMMA, ",")
            elif self.ch == '=':
                self.nextChar()
                return Token(OPERATOR, "=")
            elif self.ch == '<':
                self.nextChar()
                return Token(OPERATOR, "<")
            elif self.ch == '>':
                self.nextChar()
                return Token(OPERATOR, ">")
            elif self.ch == '$':  # EOI
                return Token(EOI, "")
            else:
                self.nextChar()
                return Token(INVALID, self.ch)

    def nextChar(self):
        self.ch = self.stmt[self.index]
        self.index = self.index + 1

    def consumeChars(self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r


class Parser:
    def __init__(self, s):
        self.lexer = Lexer(s + "$")
        self.token = self.lexer.nextToken()

    def run(self):
        self.statement()

    def statement(self):
        print("<Query>")
        if(self.token.getTokenValue() == "SELECT"):
            self.keyword()
            self.idList()
        else:
            self.error(KEYWORD)

        if(self.token.getTokenValue() == "FROM"):
            self.keyword()
            self.idList()
        else:
            self.error(KEYWORD)

        if(self.token.getTokenValue() == "WHERE"):
            self.keyword()
            self.condList()

        if(self.token.getTokenType() == EOI):
            print("</Query>")

        if(self.token.getTokenType() == INVALID):
            self.error(INVALID)
            self.token = self.lexer.nextToken()

    def idList(self):
        print("\t<IdList>")
        if(self.token.getTokenType() == ID):
            print("\t\t<Id>" + self.token.getTokenValue() + "</Id>")
            self.token = self.lexer.nextToken()
            while self.token.getTokenType() == COMMA:
                print("\t\t<Comma>,</Comma>")
                self.token = self.lexer.nextToken()
                if(self.token.getTokenType() == ID):
                    print("\t\t<Id>" + self.token.getTokenValue() + "</Id>")
                    self.token = self.lexer.nextToken()
                else:
                    self.error(ID)
        print("\t<\IdList>")

    def condList(self):
        print("\t<CondList>")
        if(self.token.getTokenType() == ID):
            self.cond()
            while self.token.getTokenValue() == "AND":
                print("\t\t<Keyword>" + self.token.getTokenValue() + "</Keyword>")
                self.token = self.lexer.nextToken()
                if(self.token.getTokenType() == ID):
                    self.cond()
                else:
                    self.error(CONDLIST)
        print("\t<\CondList>")

    def cond(self):
        print("\t\t<Cond>")
        print("\t\t\t<Id>" + self.token.getTokenValue() + "</Id>")
        self.token = self.lexer.nextToken()
        if(self.token.getTokenType() == OPERATOR):
            print("\t\t\t<Operator>" + self.token.getTokenValue() + "</Operator>")
            self.token = self.lexer.nextToken()
            self.term()
        else:
            self.error(COND)
        print("\t\t<\Cond>")

    def keyword(self):
        if(self.token.getTokenValue() == "SELECT"):
            print("\t<Keyword>SELECT<\Keyword>")
        elif(self.token.getTokenValue() == "FROM"):
            print("\t<Keyword>FROM<\Keyword>")
        elif(self.token.getTokenValue() == "WHERE"):
            print("\t<Keyword>WHERE<\Keyword>")
        elif(self.token.getTokenValue() == "AND"):
            print("\t<Keyword>AND<\Keyword>")
        self.token = self.lexer.nextToken()

    def term(self):
        if self.token.getTokenType() == ID:
            print("\t\t\t<Id>" + self.token.getTokenValue() \
                  + "</Id>")
        elif self.token.getTokenType() == INT:
            print("\t\t\t<Int>" + self.token.getTokenValue() + "</Int>")
        elif self.token.getTokenType() == FLOAT:
            print("\t\t\t<Float>" + self.token.getTokenValue() + "</Float>")
        else:
            print("Syntax error: expecting an ID, an int, or a float") \
            + "; saw:" \
            + typeToString(self.token.getTokenType())
            sys.exit(1)
        self.token = self.lexer.nextToken()

    def match(self, tp):
        val = self.token.getTokenValue()
        if (self.token.getTokenType() == tp):
            self.token = self.lexer.nextToken()
        else:
            self.error(tp)
        return val

    def error(self, tp):
        print("Syntax error: expecting: " + typeToString(tp) \
              + "; saw: " + typeToString(self.token.getTokenType()))
        sys.exit(1)


print("Testing the lexer: test 1")
lex = Lexer("SELECT C1,C2 FROM T1 WHERE C1=5.23 $")  # Creates an object
tk = lex.nextToken()
while (tk.getTokenType() != EOI):  # prints out variable
    print(tk)
    tk = lex.nextToken()
print


print("Testing the parser: test 1")
parser = Parser("SELECT C1,C2 FROM T1 WHERE C1=5.23")
parser.run()
print("Testing the parser: test 2")
parser = Parser("SELECT C1,C2 FROM T1 WHERE C1=5.23");
parser.run();
print("Testing the parser: test 3")
parser = Parser("SELECT col1, c99 FROM tab1, t2, t9");
parser.run();
print("Testing the parser: test 4")
parser = Parser("SELECT c1, c2 FROM t1, t2 WHERE c3 = 7");
parser.run();
print("Testing the parser: test 5")
parser = Parser("SELECT c1, c2 FROM t1, t2 WHERE c3<4.5");
parser.run();
print("Testing the parser: test 6")
parser = Parser("SELECT c1, c2 FROM t1, t2 WHERE c3>c123");
parser.run();
print("Testing the parser: test 7")
parser = Parser("SELECT c1 FROM t1,t2 WHERE t1a=t2a");
parser.run();
print("Testing the parser: test 8")
parser = Parser("SELECT c1 FROM t1 WHERE c2>2.78 AND c2<5.9245");
parser.run();
print("Testing the parser: test 9")
parser = Parser("SELECT c1,c2a,c3b2 FROM t1,t2,t3 WHERE c2>2.78 AND c2<5.9245 AND c3=3");
parser.run();
