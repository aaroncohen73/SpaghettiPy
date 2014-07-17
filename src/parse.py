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

reservedWords = ["auto", "break", "case", "char", "continue", "default", "do", "double", "else", "entry", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "while", "enum", "void", "const", "signed", "volatile"]

reservedNonAlphaOneChar = {";":"End of Statement" "=":"Variable Assignment" "+":"Addition" "-":"Subtraction" "*":"Multiplication/Indirection" "/":"Division" "%":"Modulo" "<":"Less Than" ">":"Greater Than" "!":"Logical Not" "~":"Bitwise Not" "&":"Bitwise And/Memory Reference" "|":"Bitwise Or" "^":"Bitwise Xor" "[":"Right Array Bracket" "]":"Left Array Bracket" ".":"Structure Reference" ",":"Comma" "{":"Begin Code Block" "}":"End Code Block" "(":"Begin grouping" ")":"End Grouping" "?":"Ternary Operator" ":":"Colon"}

reservedNonAlphaTwoChar = {"++":"Increment" "--":"Decrement" "==":"Equality Test" "!=":"Inequality Test" ">=":"Greater Than or Equal To" "<=":"Less Than or Equal To" "&&":"Logical And" "||":"Logical Or" "<<":"Bitwise Left Shift" ">>":"Bitwise Right Shift" "+=":"Addition Assignment" "-=":"Subtraction Assignment" "*=":"Multiplication Assignment" "/=":"Division Assignment" "%=":"Modulo Assignment" "&=":"Bitwise And Assignment" "|=":"Bitwise Or Assignment" "^":"Bitwise Xor Assignment" "->":"Structure Dereference"}

reservedNonAlphaThreeChar = {"<<=":"Bitwise Left Shift Assignment" ">>=":"Bitwise Right Shift Assignment"}

class Symbol(object):
    kind = ""
    value = ""

    def __init__(self, kind, value):
        self.kind = kind
        self.value = value
     
def lex(source):
"""
Lexes the source code to generate symbols for reorganization
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
                kind = "Keyword"
            else:
                kind = "Symbolic Name"

            symbols.append(Symbol(kind, value))

        elif source[i] + source[i + 1] + source[i + 2] in reservedNonAlphaThreeChar: #Tests for three-character operators
            kind = reservedNonAlphaThreeChar[source[i] + source[i + 1] + source[i + 2]]
            value = source[i] + source[i + 1] + source[i + 2]

            symbols.append(Symbol(kind, value))
            i += 2
            
        elif source[i] + source[i + 1] in reservedNonAlphaTwoChar: #Tests for two-character operators
            kind = reservedNonAlpha[source[i] + source[i + 1]]
            value = source[i] + source[i + 1]

            symbols.append(Symbol(kind, value))
            i += 1
        
        elif source[i] in reservedNonAlphaOneChar: #Tests for one-character operators
            kind = reservedNonAlpha[source[i]]
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

    return symbols
                
            
