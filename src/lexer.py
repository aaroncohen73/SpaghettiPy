#                     
#    Copyright (C) Aaron Cohen 
#                                                                     
#    This file is part of SpaghettiPy.                                                                           
#    
#    SpaghettiPy is free software: you can redistribute it and/or modify                                                         
#    it under the terms of the GNU General Public License as published by                                                       
#    the Free Software Foundation, either version 3 of the License, or                                                          
#    (at your option) any later version.
#    
#    SpaghettiPy is distributed in the hope that it will be useful,                                                            
#    but WITHOUT ANY WARRANTY; without even the implied warranty of                                                            
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                                            
#    GNU General Public License for more details.                                                                          
#                                                                                                                 
#    You should have received a copy of the GNU General Public License                                                      
#    along with SpaghettiPy.  If not, see <http://www.gnu.org/licenses/>.                                                     
#

import re

class Symbol(object):
    kind = ""
    value = ""

    def __init__(self, kind, value):
        self.kind = kind
        self.value = value
#End class Symbol

"""
Identifiers:

$v = Variable Type
$c = Conditional
$f = Flow Control
$t = Type Declaration
$l = Loop Delclaration
$i = Variable Identifier
$n = Number Literal
$m = Macro
$o = Operator
$s = String Literal
$b = Character Literal
"""

reservedWords = {"auto":"$v", "break":"$f", "case":"$c", "char":"$v", "continue":"$f", "default":"$c", "do":"$l", "double":"$v", "else":"$c", "extern":"$v", "float":"$v", "for":"$l", "goto":"$f", "if":"$c", "int":"$v", "long":"$v", "register":"$v", "return":"$f", "short":"$v", "static":"$v", "struct":"$t", "switch":"$c", "typedef":"$t", "union":"$t", "unsigned":"$v", "while":"$l", "enum":"$t", "void":"$v", "const":"$v", "signed":"$v", "volatile":"$v"}

reservedNonAlphaOneChar = [";", "=", "+", "-", "*", "/", "%", "<", ">", "!", "~", "&", "|", "^", "[", "]", ".", ",", "{", "}", "(", ")", "?", ":"]

reservedNonAlphaTwoChar = ["++", "--", "==", "!=", ">=", "<=", "&&", "||", "<<", ">>", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^", "->"]

reservedNonAlphaThreeChar = ["<<=", ">>=", "..."]

variableNameConventionsFirstLetter = "[A-Za-z_]"

variableNameConventionsNthLetter = "[A-Za-z0-9_]"

numberConventionsFirstDigit = "[0-9]"

numberConventionsNthDigit = "[0-9a-fA-FxuUlL]"
     
def lex(source):
    """
Lexes the source code to generate symbols and returns a list
    """
    symbols = []
    i = 0

    source += "\n\n\n\n\n" #Buffering the end a little

    try:
        while True:
            if source[i] == "#": #Tests for macros
                value = ""

                while True:
                    if "\n" in value and source[i] != "\\":
                        break
                    #End if

                    value += source[i]
                    i += 1
                #End while

                symbols.append(Symbol("$m", value))
            #End if

            elif source[i] + source[i + 1] == "//":
                buf = ""
                while True:
                    i += 1
                    buf += source[i]
                    if "\n" in buf:
                        break
                    #End if
                    
                #End while

            #End elif

            elif source[i] + source[i + 1] == "/*":
                i += 2
                while source[i - 1] + source[i] != "*/":
                    i += 1
                #End while

            #End elif

            elif re.match(numberConventionsFirstDigit, source[i]): #Tests for numbers
                kind = "$n"
                value = source[i]

                while re.match(numberConventionsNthDigit, source[i + 1]):
                    i += 1
                    value += source[i]
                #End while

                symbols.append(Symbol(kind, value))
            #End elif

            elif re.match(variableNameConventionsFirstLetter, source[i]): #Tests for keywords
                kind = ""
                value = source[i]

                while re.match(variableNameConventionsNthLetter, source[i + 1]):
                    i += 1
                    value += source[i]
                #End while
                
                if value in reservedWords:
                    kind = reservedWords[value]
                #End if
                else: #if value in reservedWords:
                    kind = "$i"
                #End else

                symbols.append(Symbol(kind, value))
            #End elif

            elif source[i] + source[i + 1] + source[i + 2] in reservedNonAlphaThreeChar: #Tests for three-character operators
                kind = "$o"
                value = source[i] + source[i + 1] + source[i + 2]

                symbols.append(Symbol(kind, value))
                i += 2
            #End elif

            elif source[i] + source[i + 1] in reservedNonAlphaTwoChar: #Tests for two-character operators
                kind = "$o"
                value = source[i] + source[i + 1]

                symbols.append(Symbol(kind, value))
                i += 1
            #End elif

            elif source[i] in reservedNonAlphaOneChar: #Tests for one-character operators
                kind = "$o"
                value = source[i]

                symbols.append(Symbol(kind, value))
            #End elif

            elif source[i] == '"': #Tests for string literals
                kind = "$s"
                value = ""

                i += 1
                while source[i] != '"':
                    value += source[i]
                    i += 1
                #End while

                symbols.append(Symbol(kind, value))
            #End elif

            elif source[i] == "'": #Tests for character literals
                kind = "$b"
                value = source[i + 1]

                symbols.append(Symbol(kind, value))
                i += 2
            #End elif

            elif re.match("\s", source[i]) and source[i] != "\0": #Ignore whitespace
                while True:
                    i += 1

                    try:
                        if not re.match("\s", source[i]):
                            i -= 1
                            break
                        #End if

                    #End try

                    except IndexError:
                        break
                    #End except

                #End while

            #End elif

            else: #If all else fails
                print("Error: Unrecognized Symbol %s!" % source[i])
                return None
            #End else
            i += 1
        #End while

    #End try

    except IndexError:
        print("Finished lexing")
    #End except

    symbols.append(Symbol("EOF","End of File"))
    return symbols
#End def lex(source):        
        
