# -*- coding: utf-8 -*-
import sys
from lexer import Lexer
from copy import copy, deepcopy

Lexer = Lexer()

class Frame:
    def __init__(self, parent = None):
        self._variables = {}
        self.parent = parent
        self._functions = {}

    def __setitem__(self, key, value):
        while (not isinstance(value, Literal)):
            value = value.execute(self)
        self._variables[key] = value

    def __getitem__(self, key):
        if key in self._variables:
            return self._variables[key]
        else:
            raise KeyError("Tuto promennou tu vubec nemam!! v*le.")
        

    def addFunction(self,name,args,block):
        self._functions[name] = [args, block]

    def getFunction(self,name):
        if name in self._functions:
            return [self._functions[name][0],deepcopy(self._functions[name][1])]
        else:
            if (self.parent == None):
                raise KeyError("Tuten bazmek tu vubec nemam!! v*le.")
            return self.parent.getFunction(name)

def returnOnlyLiteral(x,frame):
    while (not isinstance(x, Literal)):
        x = x.execute(frame)
    return x


class Block:
    """ Blok prikazu. 

    Nejedna se o nic jineho, nez o seznam prikazu, ktere jdou po sobe. 
    """

    def __init__(self):
        self.code = []

    def add(self, node):
        """ Prida novy prikaz. """
        self.code.append(node)

    def __str__(self):
        result = "vocat"
        for node in self.code:
            result = result + "\n" + node.__str__()
        result = result + "\npocat."
        return result

    def execute(self, frame):
        for cmd in self.code:
            cmd.execute(frame)

class BinaryOperator:
    """ Binary operator. 

    Pamatuje si levy a pravy operand a typ operace, kterou s nimi ma provest. """
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator
        
    
    def __str__(self):
        return "( %s %s %s)" % (self.left, self.operator, self.right)

    def execute(self, frame):
        left = returnOnlyLiteral(self.left,frame).execute(frame)
        right = returnOnlyLiteral(self.right,frame).execute(frame)

        if self.operator == Lexer.OP_ADD:
            try:
                try:
                    x = int(left) + int(right)
                except:
                    x = float(left) + float(right)
            except:
                if (isinstance(left, list) and not isinstance(right, list)):
                    x = left + [right]
                elif (not isinstance(left, list) and isinstance(right, list)):
                    x = [left] + right
                else:
                    x = left + right
                    
        elif self.operator == Lexer.OP_SUBTRACT:
            try:
                try:
                    x = int(left) - int(right)
                except:
                    x = float(left) - float(right)
            except:
                raise BaseException("tuhle operaci nelze provst")
        elif self.operator == Lexer.OP_MULTIPLY:
            try:
                try:
                    x = int(left) * int(right)
                except:
                    x = float(left) * float(right)
            except:
                raise BaseException("tuhle operaci nelze provst")
        elif self.operator == Lexer.OP_DIVIDE:
            try:
                try:
                    x = int(left) / int(right)
                except:
                    x = float(left) / float(right)
            except:
                raise BaseException("tuhle operaci nelze provst")
        elif self.operator == Lexer.OP_EQUALS:
            try:
                try:
                    if (int(left) == int(right)):
                        x = True
                    else:
                        x = False
                except:
                    if (float(left) == float(right)):
                        x = True
                    else:
                        x = False
            except:
                if (left == right):
                    x = True
                else:
                    x = False
        elif self.operator == Lexer.OP_BIGGER:
            try:
                try:
                    if (int(left) > int(right)):
                        x = True
                    else:
                        x = False
                except:
                    if (float(left) > float(right)):
                        x = True
                    else:
                        x = False
            except:
                raise BaseException("tuhle operaci nelze provst")
        elif self.operator == Lexer.OP_SMALLER:
            try:
                try:
                    if (int(left) < int(right)):
                        x = True
                    else:
                        x = False
                except:
                    if (float(left) < float(right)):
                        x = True
                    else:
                        x = False
            except:
                raise BaseException("tuhle operaci nelze provst")
        return Literal(x)

class FunctionPrint:
    def __init__(self, dataToPrint):
        self.dataToPrint = dataToPrint

    def __str__(self):
        return "bonzovat %s." % (self.dataToPrint,) 

    def execute(self, frame):
        print(self.dataToPrint.execute(frame))
        
class VariableRead:
    """ Cteni hodnoty ulozene v promenne. """
    def __init__(self, variableName, index = None):
        self.variableName = variableName
        self.index = index

    def __str__(self):
        if (self.index == None):
            return self.variableName
        return self.variableName+"["+str(self.index)+"]"

    def execute(self, frame):
        if (self.index == None):
            x = frame[self.variableName]
        else:
            x = frame[self.variableName]
            index = returnOnlyLiteral(self.index,frame).execute(frame)
            x = x[index]
        return x

class VariableWrite:
    """ Zapis hodnoty do promenne. Krom nazvu promenne si pamatuje i vyraz, kterym se vypocita hodnota. """
    def __init__(self, variableName, rhs):
        self.variableName = variableName
        self.rhs = rhs

    def __str__(self):
        return "%s navali %s" % (self.variableName, self.rhs)

    def execute(self, frame): 
        value = returnOnlyLiteral(self.rhs,frame)
        frame[self.variableName] = copy(value)
        
class Literal:
    """ Literal (tedy jakakoli konstanta, cislo). """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if isinstance(self.value, list):
            x = "["
            for i in self.value:
                if (x == "["):
                    x += i.__str__()
                else:
                    x += ", " + i.__str__()
            x += "]"
            return x
        else:
            return str(self.value)

    def execute(self, frame): 
        return self.value

    def __setitem__(self, key, value):
        if (isinstance(self.value, list)):
            while (not isinstance(value, Literal)):
                value = value.execute(self)
            self.value[key] = value
        else:
            raise BaseException("tohle neni seznam")

    def __getitem__(self, key):
        if (isinstance(self.value,list)):
            return self.value[key]
        else:
            raise BaseException("tohle neni seznam")

    def pop(self):
        if (isinstance(self.value, list)):
            x =  self.value.pop(0)
            return x
        else:
            raise BaseException("tohle neni seznam")

    def append(self,x):
        if (isinstance(self.value, list)):
            self.value.append(x)
            return Literal(True)
        else:
            raise BaseException("tohle neni seznam")

    def __len__(self):
        if (isinstance(self.value, list)):
            return len(self.value)
        else:
            raise BaseException("tohle neni seznam")

class If:
    """ Prikaz if. Pamatuje si vyraz ktery je podminkou a pak bloky pro true a else casti. """
    def __init__(self, condition, trueCase, falseCase):
        self.condition = condition
        self.trueCase = trueCase
        self.falseCase = falseCase

    def __str__(self): 
        return "esli %s, %s, jinac %s" % (self.condition, self.trueCase, self.falseCase)

    def execute(self,frame):
        x = returnOnlyLiteral(self.condition,frame)
        if (x.execute(frame) == True):
            self.trueCase.execute(frame)
        else:
            self.falseCase.execute(frame)

class While:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def __str__(self):
        return "dokat %s, %s" % (self.condition, self.block)

    def execute(self, frame): 
        while returnOnlyLiteral(self.condition,frame).execute(frame) == True:
            self.block.execute(frame)

class Function:
    def __init__(self, name, args, block):
        self.name = name
        self.args = args
        self.block = block

    def __str__(self):
        return "bazmek %s (%s): %s" % (self.name, self.args, self.block)

    def execute(self, frame): 
        frame.addFunction(self.name, self.args,self.block)

class FunctionCall:
    def __init__(self,name, args):
        self.name = name
        self.args = args

    def __str__(self):
        ar = []
        for i in self.args:
            ar.append(str(i))
        return "hola %s (%s)." % (self.name, ar)

    def execute(self,frame):
        (argumentnames, block) = frame.getFunction(self.name)
        if len(argumentnames) != len(self.args):
            raise BaseException("Ancal kecu nestimuje!! v*le")
        else:
            newframe = Frame (parent = frame)
            for i in xrange(0,len(self.args)):
                x = returnOnlyLiteral(self.args[i],frame)
                x = x.execute(frame)
                if (isinstance(x,list)):
                    x = deepcopy(x)
                newframe[argumentnames[i]] = Literal(x)
            try:
                block.execute(newframe)
            except Literal, e:

                return e



class Len:
    def __init__(self, ofwhat):
        self.ofwhat = ofwhat

    def __str__(self):
        return "dylka "+str(self.ofwhat)+"."

    def execute(self,frame):
        x = returnOnlyLiteral(self.ofwhat,frame)
        x = x.execute(frame)
        if isinstance(x,list):
            return Literal(len(x))
        else:
            raise BaseException("tohle neni seznam")

class Append:
    def __init__(self, where, what):
        self.where = where
        self.what = what

    def __str__(self):
        return "navalit %s do %s" % (self.what, self.where)

    def execute(self,frame):
        array = frame[self.where]
        x = returnOnlyLiteral(self.what,frame)
        array.append(x)
        frame[self.where] = array

class Pop:
    def __init__(self, what):
        self.what = what

    def __str__(self):
        return "zfajrovat %s" % (self.what,)

    def execute(self,frame): 
        x = frame[self.what]
        if (len(x)==0):
            raise BaseException("Seznam je prázdný")
        y = frame[self.what].pop()
        return y

class Return:
    def __init__(self, what):
        self.what = what

    def __str__(self):
        return "bochnot %s" % (self.what,)

    def execute(self,frame):
        x = returnOnlyLiteral(self.what, frame)
        x = x.execute(frame)
        raise Literal(x)

class For:
    def __init__(self,name,what,block):
        self.name = name
        self.what = what
        self.block = block

    def __str__(self):
        return "pro kazdy %s z %s, %s" % (self.name, self.what, self.block)

    def execute(self,frame):
        array = returnOnlyLiteral(self.what,frame)
        array2 = copy(array)
        

        for a in array2:
            frame[self.name] = a
            self.block.execute (frame)
