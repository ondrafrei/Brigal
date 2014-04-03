# -*- coding: utf-8 -*-
import sys


class Lexer:
    """ Lexikalni analyzator.
    
    Objekt, ktery se stara o lexikalni analyzu. Obsahuje v sobe vsechny druhy tokenu, a metody, ktere do tokenu umi prevest libovolny retezec. Kdyz se retezec prevede, tokeny se pridaji do seznamu tokenu. Kazdy token je tuple (typ tokenu, hodnota tokenu). Metody topToken() a popToken() slouzi k zobrazeni a posunuti se na dalsi token. Ty budeme pouzivat dale. 
    """

    EOF = "<EOF>" # typ token pro konec souboru, End Of File, oznacuje, ze uz neni zadny dalsi token za nim
    _EOF = (EOF, None) # tohle je token, je to tuple z typu, a hodnoty, hodnota EOF je zadna
    NUMBER = "number" # token pro cislo, jeho hodnotou bude hodnota cisla
    IDENT = "ident" # token pro identifikator, jeho hodnotou bude retezec s identifikatorem
    STRING = "string"
    KW_IF = "esli" # klicove slovo if 
    KW_ELSE = "jinac" # klicove slovo else
    KW_WHILE = "dokat"
    SIGN_MINUS = "-"
    OP_ADD = "plus" # operator scitani
    OP_SUBTRACT = "minus"	# odcitani
    OP_MULTIPLY = "krat"	# nasobeni
    OP_DIVIDE = "deleno"	# deleni
    OP_EQUALS = "je shodne s" # operator porovnani
    OP_BIGGER = "je vetsi nez"
    OP_SMALLER = "je mensi nez"
    OP_ASSIGN = "navali" # operator prirazeni
    KW_FUNCTION = "bazmek"
    KW_FUNCTION_CALL = "hola"
    PAR_OPEN = "("
    PAR_CLOSE = ")"
    BLOCK_START = "vocat"
    BLOCK_END = "pocat"
    BRACK_OPEN = "["
    BRACK_CLOSE = "]"
    DOT = "."
    COMMA = ","
    COLON = ":"
    NEWLINE = "\n"
    KW_RETURN = "bochnot"
    KW_PRINT = "bonzovat"
    KW_LEN = "dylka"
    KW_POP = "zfajrovat"
    KW_APPEND = "navalit"
    KW_IN = "do"
    KW_FOR = "pro kazdy"
    KW_FROM = "z"




    def __init__(self):
        """ Inicializuje lexikalni analyzator. Zalozi pole tokenu, zalozi seznam klicovych slov, atd. """
        self._tokens = [] # seznam tokenu, ktere jsme uz naparsovali
        self._keywords = {} # seznam klicovych slov. Ulozena jsou jako [klicove slovo] = typ tokenu odpovidajici
        self._keywords["esli"] = Lexer.KW_IF
        self._keywords["jinac"] = Lexer.KW_ELSE
        self._keywords["dokat"] = Lexer.KW_WHILE
        self._keywords["plus"] = Lexer.OP_ADD
        self._keywords["minus"] = Lexer.OP_SUBTRACT
        self._keywords["deleno"] = Lexer.OP_DIVIDE
        self._keywords["krat"] = Lexer.OP_MULTIPLY
        self._keywords["navali"] = Lexer.OP_ASSIGN
        self._keywords["bazmek"] = Lexer.KW_FUNCTION
        self._keywords["vocat"] = Lexer.BLOCK_START
        self._keywords["pocat"] = Lexer.BLOCK_END
        self._keywords["hola"] = Lexer.KW_FUNCTION_CALL
        self._keywords["je vetsi nez"] = Lexer.OP_BIGGER
        self._keywords["je mensi nez"] = Lexer.OP_SMALLER
        self._keywords["je shodne s"] = Lexer.OP_EQUALS
        self._keywords["bochnot"] = Lexer.KW_RETURN
        self._keywords["bonzovat"] = Lexer.KW_PRINT
        self._keywords["dylka"] = Lexer.KW_LEN
        self._keywords["zfajrovat"] = Lexer.KW_POP
        self._keywords["navalit"] = Lexer.KW_APPEND
        self._keywords["do"] = Lexer.KW_IN
        self._keywords["z"] = Lexer.KW_FROM
        self._keywords["pro kazdy"] = Lexer.KW_FOR


        self._top = 0
        self._string = ""
        self._pos = 0

        self.currentLine = 1

    def topToken(self, plus = 0):
        """ Vrati aktualni token. Vysvetlime si priste. """
        if (self._top < len(self._tokens)):
            return self._tokens[self._top + plus ]
        else:
            return Lexer._EOF

    def popToken(self):
        """ Posune se na dalsi token. Vysvetlime priste. """
        t = self.topToken()
        if (self._top < len(self._tokens)):
            self._top += 1
        return t

    def isEOF(self):
        """ Vrati true, jestlize uz zadne dalsi tokeny nejsou. Vysvetlime si priste. """
        return self._top >= len(self._tokens)

    def topChar(self):
        """ Vrati aktualne zpracovavany znak. Tohle je funkce jen proto, abychom nemuseli porad psat ten slozity pristup. """
        return self._string[self._pos]

    def popChar(self):
        """ Posune nas na dalsi znak v aktualne analyzovanem retezci, pokud takovy existuje. Zase funkce pro prehlednost, abychom nemuseli mit to kontrolovani mezi vsude. """
        if (self._pos < len(self._string)):
            self._pos += 1

    def error(self, reason):
        """ Funkce pro prehlednost, vypise ze doslo k chybe, k jake chybe doslo, a skonci program. """
        print("Krpa na lajne %s, v*le: %s " % (self.currentLine, reason ))
        sys.exit(1)

    def addToken(self, tokenType, tokenValue = None):
        """ Funkce, ktera prida dany druh tokenu a pripadne i hodnotu na seznam jiz naparsovanych tokenu. Kdyz naparsujete nejaky token, musite zavolat tuhle funkci. """
        self._tokens.append((tokenType, tokenValue, self.currentLine))

    def isLetter(self,a):
        return ((a>='a') and (a<='z')) or ((a>='A') and (a<='Z'))

    def isDigit(self,a):
        """ Funkce, ktera zjisti, jestli dany znak je cislice desitkove soustavy. """
        return (a>='0') and (a<='9')

    def isWhitespace(self,a):
        """ Funkce, ktera zjisti, jestli dany znak je whitespace. Momentalne je whitespace mezera, tab a nebo novy radek. Opacna lomitka jsou ridici znaky, kterymi muzeme zapisovat specialni znaky, ktere nejsou na klavesnici. Takze \n je konec radky, a ne opacne lomitko a male n. To by se napsalo jako \\n."""
        if (a == "\n"):
            self.currentLine += 1

        return (a in (' ','\t'))

    def skipWhitespace(self):
        """ Preskoci whitespace v aktualne zpracovavanem retezci. """
        while (self.isWhitespace(self.topChar())):
            self.popChar()

    def parseNumber(self):
        """ Naparsuje cele cislo a jeho hodnotu. """
        value = 0
        if (not self.isDigit(self.topChar())):
            self.error("Zacatek cisla musi byt cislice")
        while (self.isDigit(self.topChar())):
            value = value * 10 + (ord(self.topChar()) - ord('0'))
            self.popChar()

        if (self.topChar()=="."):
            self.popChar()
            if (not self.isDigit(self.topChar())):
                self.addToken(Lexer.NUMBER, value)
                self.addToken(Lexer.DOT)
            value = float(value)
            x=10.0
            value = value + (ord(self.topChar()) - ord('0'))/x
            self.popChar()
            while (self.isDigit(self.topChar())):
                x = x * 10
                value = value + (ord(self.topChar()) - ord('0'))/x
                self.popChar()

        self.addToken(Lexer.NUMBER, value)
    
    def parseIdentifierOrKeyword(self):
        """ Naparsuje identifikator nebo klicove slovo. Identifikator ma typ IDENT a svuj nazev jako hodnotu. Klicove slovo hodnotu nema, a typ ma podle toho, co je zac. Klicove slovo je takovy identifikator, ktery je ve slovniku klicovych slov, ktery jste inicializovali v metode __init__ nahore. """
        i = self._pos
        if (not self.isLetter(self.topChar())):
            self.error("Identifikator musi zacinat pismenem")
        while (self.isLetter(self.topChar()) or self.isDigit(self.topChar())):
            self.popChar()
        value = self._string[i : self._pos]
        if (value == "je"): # pro OP_EQUALS, BIGGER, SMALLER
            self.skipWhitespace() #prvni mezera
            while (self.isLetter(self.topChar())):
                self.popChar()

            self.skipWhitespace() #druha mezera
            while (self.isLetter(self.topChar())):
                self.popChar()
            value = self._string[i : self._pos]

            if (value == "je shodne s" or value == "je vetsi nez" or value == "je mensi nez"):
                self.addToken(self._keywords[value])
                return
            else:
                print value
                self.error("Po 'je' muze kur*a prijit enom 'vetsi nez', 'mensi nez' nebo 'shodne s'!! v*le")
        elif (value == "pro"): # kw_for
            self.skipWhitespace() #prvni mezera
            while (self.isLetter(self.topChar())):
                self.popChar()
            value = self._string[i : self._pos]
            if (value == "pro kazdy"):
                self.addToken(self._keywords[value])
                return
            else:
                self.error("Po 'pro' muzes napsat leda 'kazdy'!! v*le")


        if (value in self._keywords):
            self.addToken(self._keywords[value])
        else:
            self.addToken(Lexer.IDENT, value)

    
    def analyzeString(self, string):
        """ Rozkouskuje dany retezec na tokeny. Nastavi aktualne zpracovavany retezec na ten co funkci posleme, vynuluje aktualni pozici a vola funkci pro naparsovani tokenu dokuc neni cely retezec analyzovan. """
        self._string = string + "\0" # na konec retezce pridame znak s kodem 0 (to neni 0 jako cifra, ale neviditelny znak). Ten se nesmi v retezci vyskytovat a my s nim jednoduse poznavame, ze jsme na konci. 
        self._pos = 0
        while (self._pos < len(self._string)):
            self.parseToken()

    def parseToken(self):
        """ Naparsuje jeden token ze vstupniho retezce. Preskoci whitespace a pak se rozhodne jestli se jedna o cislo, identifikator, klicove slovo, operator, atd. a overi ze je vse v poradku. Token prida do seznamu naparsovanych tokenu. """
        self.skipWhitespace()
        c = self.topChar()
        if (self.isLetter(c)):
            self.parseIdentifierOrKeyword()

        elif (self.isDigit(c)):
            self.parseNumber()

        elif (c == '('):
            self.popChar()
            self.addToken(Lexer.PAR_OPEN)

        elif (c == ')'):
            self.popChar()
            self.addToken(Lexer.PAR_CLOSE)

        elif (c == '['):
            self.popChar()
            self.addToken(Lexer.BRACK_OPEN)

        elif (c == ']'):
            self.popChar()
            self.addToken(Lexer.BRACK_CLOSE)

        elif (c == '.'):
            self.popChar()
            self.addToken(Lexer.DOT)

        elif (c == ','):
            self.popChar()
            self.addToken(Lexer.COMMA)

        elif (c == ':'):
            self.popChar()
            self.addToken(Lexer.COLON)

        elif (c == '\n'):
            self.popChar()
            self.addToken(Lexer.NEWLINE)

        elif (c == '-'):
            self.popChar()
            self.addToken(Lexer.SIGN_MINUS)


        elif (c == '\0'):
            self._pos += 1
            pass

        else:
            self.error("Cizi lejno u vrat!")
