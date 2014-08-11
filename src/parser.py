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

#Begin imports

from lexer import Symbol

#End imports

class Statement(object):
    kind = ""
    plaintext = ""
    line = 0

    def __init__(self, kind, plaintext, line):
        self.kind = kind
        self.plaintext = plaintext
        self.line = line
#End class Statement

def parse(symbols):
    """
Parses a list of symbols and returns a list of statements
    """
    statements = [] #List of statements to return
    i = 0 #Index in the list of statements
    currentLine = 0; #Current line number (Separates each statement onto a separate line
    
    try:
        while True:
            if symbols[i].kind == "$m": #Statement is a macro
                statements.append(Statement("Macro", symbols[i].value, currentLine))
                currentLine += 1
            #End if
            
            if symbols[i].kind == "$i": #This is a reassignment, function call, or struct member access call
                
                statement = ""
                kind = ""
                j = 1

                while symbols[i + j].value != "=":
                    if symbols[i + j].value == ";":
                        kind = "Function Call"
                        break
                    j += 1
                #End while

                if kind == "":
                    kind = "Variable Reassignment"
                #End if

                while symbols[i].value != ";":
                    statement += symbols[i].value
                    i += 1
                #End while

                statement += ";"
                statements.append(Statement(kind, statement, currentLine))
                currentLine += 1
            #end elif

            elif symbols[i].kind == "$v": #Either a variable declaration/initialization, a function pointer, or a function declaration
                j = i #Index in the declaration statement
                statement = symbols[j].value #The statement being created (Plaintext)
                j += 1

                while symbols[j].kind == "$v" or symbols[j].value == "*":
                    statement += " " + symbols[j].value
                    j += 1
                #End while

                if symbols[j].kind == "$i": #This is a variable declaration and/or initialization
                    i = j #Saving the symbolic name just in case this is a function pointer
                    statement += " " + symbols[j].value
                    if symbols[j + 1].value != "(":
                        statements.append(Statement("Variable Declaration", statement + ";", currentLine))

                        if symbols[j + 1].value == "=": #Separates the variable declaraction and initializations onto separate lines
                            currentLine += 1

                            statement = symbols[j].value + " ="  #The statement being created (Plaintext)
                            k = j + 2 #Index in the initialization statement

                            initStatements = [] #For fixing the ordering issue in multiple initialization

                            while symbols[k].value != ";":
                                if symbols[k].value == "=": #In the case of variable = variable2 = 3
                                    initStatements.append(Statement("Variable Initialization", statement + ";", currentLine))
                                    currentLine += 1 #Not in the right order. Fix later.
                                    statement = symbols[k - 1].value + " ="
                                #End if

                                statement += " " + symbols[k].value;
                                k += 1
                            #End while
                            
                            initStatements.append(Statement("Variable Initialization", statement + ";", currentLine))
                            currentLine += 1
                            for index in reversed(range(0, len(initStatements))):
                                statements.append(initStatements[index])
                            #End for
                            
                            i = k
                        #End if

                        else:
                            i = j + 1
                        #End else
                    #End if

                    else: #This is either a function declaration or a prototype
                        j += 2
                        lcount = 1

                        statement += " ("

                        while lcount != 0:
                            statement += " " + symbols[j].value
                            if symbols[j].value == "(":
                                lcount += 1
                            #End if

                            elif symbols[j].value == ")":
                                lcount -= 1
                            #End elif

                            j += 1
                        #End while

                        if symbols[j].value == ";": #This is a function prototype
                            statements.append(Statement("Function Prototype", statement, currentLine))
                            currentLine += 1
                        #End if

                        else: #This is a function declaration (We will use the code block later
                            statements.append(Statement("Function Declaration", statement, currentLine))
                            currentLine += 1
                        #End else

                        i = j - 1

                    #End else

                #End if

                elif symbols[j].value == "(": #This is a function pointer
                    while symbols[j].value != ";" and symbols[j].value != "=":
                        statement += " " + symbols[j].value
                        j += 1
                    #End while

                    statements.append(Statement("Function Pointer Declaration", statement + ";", currentLine))
                    currentLine += 1

                    if symbols[j].value == "=": #The pointer is initialized in the same statement
                        statement = symbols[i].value + " =" #Using i for two things at once
                        j += 1

                        while symbols[j].value != ";":
                            statement += " " + symbols[j].value
                            j += 1
                        #End while

                        statements.append(Statement("Function Pointer Initialization", statement, currentLine))
                        currentLine += 1
                        i = j
                    #End if

                #End elif

            #End elif

            elif symbols[i].kind == "$l": #This is the beginning of a loop
                statement = ""

                if symbols[i].value != "do": #Because "do" takes no arguments, but while does
                    statement = symbols[i].value
                    i += 1
                    statement += " " + symbols[i].value #The left parenthesis
                    i += 1

                    lcount = 1

                    while lcount != 0:
                        statement += " " + symbols[i].value
                        if symbols[i].value == "(":
                            lcount += 1
                        #End if

                        elif symbols[i].value == ")":
                            lcount -= 1
                        #End elif

                        i += 1
                    #End while
                #End if

                else: #If it is a do-while loop
                    statement = symbols[i].value
                #End else

                statements.append(Statement("Loop Declaration", statement, currentLine))
                currentLine += 1
            #end elif

            elif symbols[i].kind == "$c": #This is a conditional branching statement
                if symbols[i].value == "case" or symbols[i].value == "default":
                    statement = symbols[i : i + 2].value.join(" ")
                    i += 2
                #End if

                elif symbols[i].value == "else":
                    statement = symbols[i].value
                #End elif

                else:
                    statement = symbols[i].value
                    i += 1
                    statement += " " + symbols[i].value
                    i += 1

                    lcount = 1

                    while lcount != 0:
                        statement += " " + symbols[i].value
                        if symbols[i].value == "(":
                            lcount += 1
                        #End if

                        elif symbols[i].value == ")":
                            lcount -= 1
                        #End elif

                        i += 1
                    #End while

                #End else

                statements.append(Statement("Conditional Branching Statement", statement, currentLine))

                if "case" in statements[-1].value or "default" in statements[-1].value:
                    statements.append(Statement("Begin Code Block", "{", ++currentLine))

                    i += 1
                    lbrace = 0
                    caseSymbols = []
                    
                    while True:
                        if symbols[i].value == "{":
                            lbrace += 1
                        #End if

                        elif symbols[i].value == "}":
x                            lbrace -= 1
                        #End elif

                        if symbols[i].value == "break" and lbrace == 0:
                            break
                        #End if

                        caseSymbols += symbols[i]
                    #End while

                    statements.append(parse(caseSymbols))
                    statements.append("End Code Block", "}", ++currentLine))
                #End if
                
                currentLine += 1
            #end elif

            elif symbols[i].kind == "$f": #This is a flow control statement
                statement = symbols[i].value

                if symbols[i].value == "goto" or symbols[i].value == "return":
                    i += 1
                    while symbols[i].value != ";":
                        statement += " " + symbols[i].value
                        i += 1
                    #End while

                    statement += symbols[i].value
                #End if

                else:
                    i += 1
                    statement += symbols[i].value
                #End else

                statements.append(Statement("Flow Control Statement", statement, currentLine))
                currentLine += 1
            #end elif

            elif symbols[i].kind == "$t": #This is a type declaration
                statement = ""

                if symbols[i].value == "typedef":
                    statement += symbols[i].value
                    i += 1
                #End if

                while symbols[i].value != "}":
                    statement += " " + symbols[i].value
                    i += 1
                #End while

                while symbols[i].value != ";":
                    statement += " " + symbols[i].value
                    i += 1
                #End while

                statement += ";"
                statements.append(Statement("Type Definition", statement, currentLine))
                currentLine += 1
            #end elif

            elif symbols[i].value == "{":
                statement = symbols[i].value
                statements.append(Statement("Begin code block", statement, currentLine))
                currentLine += 1
            #End elif

            elif symbols[i].value == "}":
                statement = symbols[i].value
                statements.append(Statement("End code block", statement, currentLine))
                currentLine += 1
            #End elif
            
            i += 1
        #End while

    #End try

    except IndexError:
        print("Finished parsing")
    #End except
        
    return statements
#End def parse(symbols):

