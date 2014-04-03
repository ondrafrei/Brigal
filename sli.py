from ast import Frame
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
    inputString = """ bazmek quicksort ( seznam ):
    vocat
        x navali dylka seznam.
        esli x je mensi nez 2 ,
            vocat
                bochnot seznam.
            pocat,
        jinac
            vocat
                
                pivot navali zfajrovat seznam.
                haranti navali [].
                borci navali [].
                i navali 0 .
                a navali dylka seznam.
                dokat i je mensi nez a,
                    vocat
                        esli seznam[i] je mensi nez pivot,
                            vocat
                                navalit seznam[i] do haranti.
                            pocat,
                        jinac
                            vocat
                                navalit seznam[i] do borci.
                            pocat.
                        i navali i plus 1 .
                    pocat.

                vystup navali hola quicksort (haranti) plus pivot plus hola quicksort (borci).
                bochnot vystup.

            pocat.
    pocat.

    a navali [8,7,546565,67987,24,6843,65,654621,84,54].
    b navali hola quicksort(a).
    bonzovat a.
    bonzovat b.
    """

    l = Lexer()
    l.analyzeString(inputString)
    p = Parser(l)
    ast = p.parse()

    print "\n"
    f = Frame()
    ast.execute(f) 

    print "\n"

testParser()
