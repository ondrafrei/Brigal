from frame import Frame
from lexer import Lexer
# jmenuje se slparser (Simple Language Parser), aby se netriskal s pythonim modulem parser
from slparser import Parser


def testLexer():
	""" Ukazka pouziti lexeru. """
	s = " esli (kocka je ziva) potom pes dela haf. jinac potom pes dela kulovy."
        l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
	l.analyzeString(s) # timhle mu reknete, aby naparsoval string, ktery jste napsali
	while (not l.isEOF()): # tohle slouzi k vypsani vsech tokenu
		print(l.popToken())

def testParser():
        #s = " esli (kocka je ziva) potom pes dela haf. jinac potom pes dela kulovy."
        s = "jdisa dela 3 = 1 hovno dela 2 vytiskni(jdisa)"
	l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
	l.analyzeString(s) # timhle mu reknete, aby naparsoval string, ktery jste napsali
	p = Parser(l) # zalozim si parser a dam mu lexer ze ktereho bude cist tokeny
	ast = p.parse() # naparsuju co mam v lexeru a vratim AST 
	print(ast) # zobrazim ten strom
	f = Frame()
	ast.execute(f)

#testLexer()
testParser()
