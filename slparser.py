# -*- coding: utf-8 -*-
from ast import *
from lexer import Lexer

class Parser:
    """ Jednoduchy priklad parseru. Naparsuje nasledujici gramatiku

    Ten parser se trosku lisi od toho parseru, ktery jsme delali na hodine, protoze uz pouziva ty jednoduzsi stromy, o kterych jsem mluvil. Takze misto toho, aby kazde pravidlo melo svoji vlasti tridu (v ast), tak ty tridy pro ten strom odpovidaji spis tomu, co ten program bude delat, nez tomu, jak je napsana gramatika. Blizsi popisky viz jednotlive parsovaci metody nize.
    """


    def __init__(self, lexer):
        """ Zalozi parser a zapamatuje si lexer, se kterym bude pracovat. """
        self.lexer = lexer
        pass

    def pop(self, type = None):
        """ Abych nemusel tolik psat, provede pop z lexeru. Kdyz specifikuju druh tokenu, ktery ocekavam, tak zaroven zkontroluje jestli je to spravny typ, a vyhodi vyjimku, kdyz tomu tak neni. 
        """
        if (type is None):
            return self.lexer.popToken()
        t = self.lexer.topToken()
        if (t[0] == type):
            return self.lexer.popToken()
        else:
            raise SyntaxError("Ocekavany token " + type + " neni na vstupu " + t[0] + " misto nej na radku "+str(t[2])+".")

    def top(self, plus = 0):
        """ Abych nemusel tolik psat, provede top() z lexeru. 
        """
        return self.lexer.topToken(plus)

    def parse(self):
        """ Hlavni metoda na parsovani, odpovida pravidlu pro program:

        PROGRAM ::= { STATEMENT }

        Z hlediska stromu (ast) je program tedy blok prikazu, postupne jak prikazy parsuju tak je pridavam do toho bloku. Kdyz zjistim, ze uz na vstupu zadny token nemam, tak jsem skoncil.
        """
        program = Block()
        while (self.top()[0] != Lexer.EOF):
            self.popNewline()
            program.add(self.parseStatement())
            if (self.top()[0] == Lexer.EOF):
                return program
            self.pop(Lexer.DOT)
            self.popNewline()
        return program

    def parseStatement(self):
        if (self.top()[0] == Lexer.KW_IF): 
            return self.parseIf()
        elif (self.top()[0] == Lexer.KW_WHILE):
            return self.parseWhile()
        elif (self.top()[0] == Lexer.KW_FOR):
            return self.parseFor()
        elif (self.top()[0] == Lexer.KW_FUNCTION): 
            return self.parseFunction()

        elif (self.top()[0] == Lexer.KW_APPEND): 
            return self.parseAppend()
        elif (self.top()[0] == Lexer.KW_LEN): 
            return self.parseLen()



        elif (self.top()[0] == Lexer.BLOCK_START):
            return self.parseBlock()
        elif (self.top()[0] == Lexer.KW_PRINT):
            return self.parsePrint()
        elif (self.top()[0] == Lexer.KW_RETURN):
            return self.parseReturn()
        elif (self.top()[0] == Lexer.KW_POP):
            return self.parsePop()
        elif (self.top()[0] == Lexer.KW_LEN):
            return self.parseLen()
        elif (self.top()[0] == Lexer.KW_APPEND):
            return self.parseAppend()
        elif (self.top()[0] == Lexer.KW_FUNCTION_CALL):
            return self.parseFunctionCall()
        else:
            return self.parseAssignment()

    def parseAssignment(self):
        """ ASSIGNMENT ::= ident op_assign EXPRESSION
       
        Ulozeni hodnoty do promenne vypada tak, ze na leve strane je identifikator promenne, hned za nim je operator prirazeni a za nim je vyraz, ktery vypocitava hodnotu, kterou do promenne chci ulozit. Tohle je zjednodusena verze prirazeni, viz komentare k hodine. 
        """
        variableName = self.pop(Lexer.IDENT)[1]
        self.pop(Lexer.OP_ASSIGN)
        rhs = self.parseExpression()
        return VariableWrite(variableName, rhs)

    def parseExpression(self):
        lhs = self.parseE1()
        while (self.top()[0] == Lexer.OP_EQUALS):
            op = self.pop()[0]
            rhs = self.parseE1()
            lhs = BinaryOperator(lhs, rhs, op)
        return lhs
    
    def parseE1(self):
        lhs = self.parseE2()
        while (self.top()[0] in (Lexer.OP_BIGGER, Lexer.OP_SMALLER)):
            op = self.pop()[0]
            rhs = self.parseE2()
            lhs = BinaryOperator(lhs, rhs, op)
        return lhs

    def parseE2(self):
        lhs = self.parseE3()
        while (self.top()[0] in (Lexer.OP_ADD, Lexer.OP_SUBTRACT)):
            op = self.pop()[0]
            rhs = self.parseE3()
            lhs = BinaryOperator(lhs, rhs, op)
        return lhs

    def parseE3(self):

        lhs = self.parseE4()
        while (self.top()[0] in (Lexer.OP_MULTIPLY, Lexer.OP_DIVIDE)):
            op = self.pop()[0]
            rhs = self.parseE4()
            lhs = BinaryOperator(lhs, rhs, op)
        return lhs

    def parseE4(self):
        if (self.top()[0] == Lexer.SIGN_MINUS):
            self.pop(Lexer.SIGN_MINUS)[0]
            rhs = self.parseF()
            lhs = BinaryOperator(Literal(0), rhs, Lexer.OP_SUBSTRACT)
        else:
            lhs = self.parseF()
        return lhs

    def parseF(self):
        """Faktorem vyrazu pak je bud cislo (literal), nebo nazev promenne, v tomto pripade se vzdycky jedna o cteni promenne a nebo znova cely vyraz v zavorkach. 
        """
        if (self.top()[0] == Lexer.NUMBER):
            value = self.pop()[1]
            return Literal(value)
        elif (self.top()[0] == Lexer.KW_LEN):
            return self.parseLen() 
        elif (self.top()[0] == Lexer.KW_POP):
            return self.parsePop()
        elif (self.top()[0] == Lexer.KW_RETURN):
            return self.parseReturn()
        elif (self.top()[0] == Lexer.IDENT):
            variableName = self.pop()[1]
            if (self.top()[0] == Lexer.BRACK_OPEN):
                self.pop(Lexer.BRACK_OPEN)
                index = self.parseF()
                self.pop(Lexer.BRACK_CLOSE)
            else:
                index = None
            return VariableRead(variableName, index=index)
        elif (self.top()[0] == Lexer.BRACK_OPEN):
            return self.parseArray()
        elif (self.top()[0] == Lexer.KW_FUNCTION_CALL):
            return self.parseFunctionCall()

        else:
            self.pop(Lexer.PAR_OPEN)
            result = self.parseExpression()
            self.pop(Lexer.PAR_CLOSE)
            return result 

    def parseIf(self):
        """ IF_STATEMENT ::= if op_paropen EXPRESSION op_parclose [ BLOCK ] [ else BLOCK ]
        
        If podminka je klasicky podminka a za ni if, pripadne else block. Vsimnete si, ze oba dva jsou vlastne v moji gramatice nepovinne. 
        """
        self.pop(Lexer.KW_IF)
        
        condition = self.parseExpression()

        self.pop(Lexer.COMMA)
        self.popNewline()
        
        trueCase = Block() # to aby se nam chybeji vetev sprave zobrazila jako {}

        falseCase = Block() # to aby se nam chybeji vetev sprave zobrazila jako {}

        
        trueCase = self.parseBlock() # po podmínce musí být block 

        try:
            if (self.top(1)[0] == Lexer.KW_ELSE): 
                self.pop(Lexer.COMMA)
                self.pop(Lexer.KW_ELSE)
                self.popNewline()
                falseCase = self.parseBlock()
            elif (self.top(2)[0] == Lexer.KW_ELSE): 
                self.pop(Lexer.COMMA)
                self.popNewline()
                self.pop(Lexer.KW_ELSE)
                self.popNewline()
                falseCase = self.parseBlock()
        except:
            pass

        
        return If(condition, trueCase, falseCase)

    def parseBlock(self):
        """ BLOCK ::= op_braceopen { STATEMENT } op_braceclose

        Blok je podobny programu, proste nekolik prikazu za sebou. 
        """
        self.pop(Lexer.BLOCK_START)
        self.popNewline()
        result = Block()
        while (self.top()[0] != Lexer.BLOCK_END):
            result.add(self.parseStatement())
            self.pop(Lexer.DOT)
            self.popNewline()
        self.pop(Lexer.BLOCK_END)
        return result

    def parseWhile (self):
        self.pop(Lexer.KW_WHILE)
        condition = self.parseExpression()
        self.pop(Lexer.COMMA)
        self.popNewline()
        block = self.parseBlock()
        return While(condition, block)

    def parsePrint (self):
        self.pop(Lexer.KW_PRINT)
        what = self.parseExpression()
        return FunctionPrint(what)

    def parseArray (self):
        self.pop(Lexer.BRACK_OPEN)
        array = []
        while(self.top()[0] != Lexer.BRACK_CLOSE):
            array.append(self.parseExpression())
            if self.top()[0] == Lexer.COMMA:
                self.pop(Lexer.COMMA)
        self.pop(Lexer.BRACK_CLOSE)

        return Literal(array)

    def parseFunction (self):
        self.pop(Lexer.KW_FUNCTION)
        name = self.pop(Lexer.IDENT)[1]
        self.pop(Lexer.PAR_OPEN)
        args = []
        while (self.top()[0] != Lexer.PAR_CLOSE):
            args.append(self.pop(Lexer.IDENT)[1])
            if self.top()[0] == Lexer.COMMA:
                self.pop(Lexer.COMMA)
        self.pop(Lexer.PAR_CLOSE)
        self.pop(Lexer.COLON)
        self.popNewline()
        block = self.parseBlock()
        return Function(name,args,block)

    def parseFunctionCall (self):
        self.pop(Lexer.KW_FUNCTION_CALL)
        name = self.pop(Lexer.IDENT)[1]
        self.pop (Lexer.PAR_OPEN)
        args = []
        while (self.top()[0] != Lexer.PAR_CLOSE):
            args.append(self.parseExpression())
            if self.top()[0] == Lexer.COMMA:
                self.pop(Lexer.COMMA)
        self.pop(Lexer.PAR_CLOSE)
        return FunctionCall(name,args)

    def popNewline(self):
        while (self.top()[0] == Lexer.NEWLINE):
            self.pop(Lexer.NEWLINE)

    def parseLen(self):
        self.pop(Lexer.KW_LEN)
        ofwhat = self.parseF()
        return Len(ofwhat)

    def parseAppend(self):
        self.pop(Lexer.KW_APPEND)
        what = self.parseExpression()
        self.pop(Lexer.KW_IN)
        where = self.pop(Lexer.IDENT)[1]
        return Append(where, what)

    def parsePop(self):
        self.pop(Lexer.KW_POP)
        what = self.pop(Lexer.IDENT)[1]
        return Pop(what)

    def parseReturn(self):
        self.pop(Lexer.KW_RETURN)
        what = self.parseExpression()
        return Return(what)

    def parseFor(self):
        self.pop(Lexer.KW_FOR)
        name = self.pop(Lexer.IDENT)[1]
        self.pop(Lexer.KW_FROM)
        what = self.parseExpression()
        self.pop(Lexer.COMMA)
        self.popNewline()
        block = self.parseBlock()
        return For(name, what, block)
