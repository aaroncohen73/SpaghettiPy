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

"""
Identifiers:
%v = Variable Type
%c = Conditional
%f = Flow Control
%m = Variable Modifier
%t = Type Declaration
%l = Loop Delclaration
%i = Variable Identifier
"""

reservedWords = {"auto":"%m", "break":"%f", "case":"%c", "char":"%v", "continue":"%f", "default":"%c", "do":"%l", "double":"%v", "else":"%c", "extern":"%m", "float":"%v", "for":"%l", "goto":"%f", "if":"%c", "int":"%v", "long":"%v", "register":"%m", "return":"%f", "short":"%v", "static":"%m", "struct":"%t", "switch":"%c", "typedef":"%t", "union":"%t", "unsigned":"%v", "while":"%l", "enum":"%t", "void":"%v", "const":"%m", "signed":"%v", "volatile":"%m"}

reservedNonAlphaOneChar = {";", "=", "+", "-", "*", "/", "%", "<", ">", "!", "~", "&", "|", "^", "[", "]", ".", ",", "{", "}", "(", ")", "?", ":"}

reservedNonAlphaTwoChar = {"++", "--", "==", "!=", ">=", "<=", "&&", "||", "<<", ">>", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^", "->"}

reservedNonAlphaThreeChar = {"<<=", ">>="}
     
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
                
            symbols.append(Symbol("Macro", value))
            
        elif source[i].isDigit() is True: #Tests for numbers
            kind = ""
            value = ""
            
            if source[i + 1] is "x":
                kind = "Hexadecimal"
            else:
                kind = "Decimal"

            while source[i].isDigit() is True:
                value.append(source[i])
                i += 1
                
            symbols.append(Symbol(kind, value))

        elif source[i].isAlpha() is True: #Tests for keywords
            kind = ""
            value = ""

            while source[i].isAlpha() is True:
                value.append(source[i])
                i += 1

            if value in reservedWords:
                kind = reservedWords[value]
            else:
                kind = "Symbolic Name"
                
            symbols.append(Symbol(kind, value))

        elif source[i] + source[i + 1] + source[i + 2] in reservedNonAlphaThreeChar: #Tests for three-character operators
            kind = "Symbol"
            value = source[i] + source[i + 1] + source[i + 2]

            symbols.append(Symbol(kind, value))
            i += 2
            
        elif source[i] + source[i + 1] in reservedNonAlphaTwoChar: #Tests for two-character operators
            kind = "Symbol"
            value = source[i] + source[i + 1]

            symbols.append(Symbol(kind, value))
            i += 1
        
        elif source[i] in reservedNonAlphaOneChar: #Tests for one-character operators
            kind = "Symbol"
            value = source[i]

            symbols.append(Symbol(kind, value))

        elif source[i] is "\"": #Tests for string literals
            kind = "String Literal"
            value = ""
            
            i += 1
            while source[i] is not "\"":
                value.append(source[i])
                i += 1

            symbols.append(Symbol(kind, value))

        elif source[i] is "\'": #Tests for character literals
            kind = "Character Literal"
            value = source[i + 1]

            symbols.append(Symbol(kind, value))
            i += 2

        else: #If all else fails
            print("Error: Unrecognized Symbol!")
            return None
            
        i += 1

    symbols.append(Symbol("EOF","End of File"))
    return symbols
                
            
