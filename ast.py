# -*- coding: utf-8 -*-
import sys
		
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
		result = "{"
		for node in self.code:
			result = result + "\n" + node.__str__()
		result = result + "\n }\n"
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
                left = self.left.execute(frame)
                right = self.right.execute(frame)
                if self.operator == "+":
                        return left + right
                elif self.operator == "-":
                        return left - right
                elif self.operator == "*":
                        return left * right
                elif self.operator == "/":
                        return left / right

class FunctionPrint:
        def __init__(self, dataToPrint):
                self.dataToPrint = dataToPrint

        def execute(self, frame):
                print(self.dataToPrint.execute(frame))
        
class VariableRead:
	""" Cteni hodnoty ulozene v promenne. """
	def __init__(self, variableName):
		self.variableName = variableName

	def __str__(self):
		return self.variableName

	def execute(self, frame):
                try:
                        return frame[self.variableName]
                except KeyError:
                        print("Variable named %s does not exist." % self.variableName)
                        sys.exit(1)

class VariableWrite:
	""" Zapis hodnoty do promenne. Krom nazvu promenne si pamatuje i vyraz, kterym se vypocita hodnota. """
	def __init__(self, variableName, rhs):
		self.variableName = variableName
		self.rhs = rhs

	def __str__(self):
		return "%s = %s" % (self.variableName, self.rhs)

	def execute(self, frame):
                value = self.rhs.execute(frame)
                frame[self.variableName] = value
        
class Literal:
	""" Literal (tedy jakakoli konstanta, cislo). """
	def __init__(self, value):
		self.value = str(value)

	def __str__(self):
		return self.value

	def execute(self, frame):
                return self.value

class If:
	""" Prikaz if. Pamatuje si vyraz ktery je podminkou a pak bloky pro true a else casti. """
	def __init__(self, condition, trueCase, falseCase):
		self.condition = condition
		self.trueCase = trueCase
		self.falseCase = falseCase

	def __str__(self):
		return "if (%s) %s else %s" % (self.condition, self.trueCase, self.falseCase)





