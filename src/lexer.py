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

from types import Symbol

import re

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

reservedNonAlphaThreeChar = ["<<=", ">>="]

variableNameConventionsFirstLetter = "[A-Za-z_]"

variableNameConventionsNthLetter = "[A-Za-z0-9_]"

numberConventionsFirstDigit = "[0-9]"

numberConventionsNthDigit = "[0-9a-fA-FxfuUlL]"
     
def lex(source):
"""
Lexes the source code to generate symbols and returns a list
"""
    symbols = []
    i = 0
    
    while source[i] is not None:
        if source[i] is "#": #Tests for macros
            value = ""
            
            while i is not "\n":
                value.append(source[i])
                i += 1
            #End while

            #Still need to implement multiline macros
            symbols.append(Symbol("$m", value))
        #End if
            
        elif re.match(numberConventionsFirstDigit, source[i]) is not None: #Tests for numbers
            kind = "$n"
            value = source[i]
            i += 1

            while re.match(numberConventionsNthDigit, source[i]) is not None:
                value.append(source[i])
                i += 1
            #End while
                
            symbols.append(Symbol(kind, value))
        #End elif
        
        elif re.match(variableNameConventionsFirstLetter, source[i]) is not None: #Tests for keywords
            kind = ""
            value = source[i]

            while re.match(variableNameConventionsNthLetter, source[i]) is not None:
                value.append(source[i])
                i += 1
            #End while

            if value in reservedWords:
                kind = reservedWords[value]
            #End if
            else: #if value in reservedWords:
                kind = "$i"
            #End else
                
            symbols.append(Symbol(kind, value))
        #End elif
            
        elif source[i, i + 2] in reservedNonAlphaThreeChar: #Tests for three-character operators
            kind = "$o"
            value = source[i, i + 2]

            symbols.append(Symbol(kind, value))
            i += 2
        #End elif
            
        elif source[i, i + 1] in reservedNonAlphaTwoChar: #Tests for two-character operators
            kind = "$o"
            value = source[i, i + 1]

            symbols.append(Symbol(kind, value))
            i += 1
        #End elif
        
        elif source[i] in reservedNonAlphaOneChar: #Tests for one-character operators
            kind = "$o"
            value = source[i]

            symbols.append(Symbol(kind, value))
        #End elif

        elif source[i] is "\"": #Tests for string literals
            kind = "$s"
            value = ""
            
            i += 1
            while source[i] is not "\"":
                value.append(source[i])
                i += 1
            #End while

            symbols.append(Symbol(kind, value))
        #End elif

        elif source[i] is "\'": #Tests for character literals
            kind = "$b"
            value = source[i + 1]

            symbols.append(Symbol(kind, value))
            i += 2
        #End elif

        elif re.match("\s", source[i] is not None: #Ignore whitespace
            pass
        #End elif
            
        else: #If all else fails
            print("Error: Unrecognized Symbol!")
            return None
        #End else
            
        i += 1
    #End while

    symbols.append(Symbol("EOF","End of File"))
    return symbols
#End def lex(source):        
        
