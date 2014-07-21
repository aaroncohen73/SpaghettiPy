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

import lexer

Symbol = lexer.Symbol

class Statement(object):
    kind = ""
    plaintext = ""
    line = 0

    def __init__(self, kind, plaintext, line):
        self.kind = kind
        self.plaintext = plaintext
        self.line = line

def parse(symbols):
    """
Parses a list of symbols and returns a list of statements
    """
    statements = [] #List of statements to return
    i = 0 #Index in the list of statements
    currentLine = 0; #Current line number (Separates each statement onto a separate line

    while symbols[i].kind is not "EOF":
        if symbols[i].kind is "Macro": #Statement is a macro
            statements.append(types.Statement("Macro", symbols[i].value, currentLine))
            currentLine += 1
        #End if

        elif symbols[i].kind is "$v": #Either a variable declaration/initialization, a function pointer, or a function declaration
            j = i #Index in the declaration statement
            statement = symbols[j].value #The statement being created (Plaintext)
            j += 1
            
            while symbols[j].kind is "$v" or symbols[j].value is "*":
                statement += " " + symbols[j].value
                j += 1
            #End while

            if symbols[j].kind is "$i": #This is a variable declaration and/or initialization
                i = j #Saving the symbolic name just in case this is a function pointer
                statement.append(" " + symbols[j].value)
                if symbols[j + 1].value is not "(":
                    statements.append(types.Statement("Variable Declaration", statement + ";", currentLine))
                        
                    if symbols[j + 1].value is "=": #Separates the variable declaraction and initializations onto separate lines
                        currentLine += 1
                        
                        statement = symbols[j].value + " ="  #The statement being created (Plaintext)
                        k = j + 2 #Index in the initialization statement

                        initStatements = [] #For fixing the ordering issue in multiple initialization
                        
                        while symbols[k].value is not ";":
                            if symbols[k].value is "=": #In the case of variable = variable2 = 3
                                initStatements.append(types.Statement("Variable Initialization", statement + ";", currentLine))
                                currentLine += 1 #Not in the right order. Fix later.
                                statement = symbols[k - 1].value + " ="
                            #End if
                            
                            statement.append(" " + symbols[k].value());
                            k += 1
                        #End while

                        statement += symbols[k]
                        initStatements.append(types.Statement("Variable Initialization", statement, currentLine))
                        currentLine += 1
                        statements.append(initStatements.reverse()) #Putting multiple initializations on the correct lines
                        i = k
                    #End if
                        
                    else:
                        i = j + 1
                    #End else
                #End if
                
                else: #This is either a function declaration or a prototype
                    j += 2
                    lcount = 1

                    statement.append(" (")
                    
                    while lcount is not 0:
                        statement.append(" " + symbols[j].value)
                        if symbols[j].value is "(":
                            lcount += 1
                        #End if
                            
                        elif symbols[j].value is ")":
                            lcount -= 1
                        #End elif
                            
                        j += 1
                    #End while

                    if symbols[j].value is ";": #This is a function prototype
                        statements.append(types.Statement("Function Prototype", statement, currentLine))
                        currentLine += 1
                    #End if
                    
                    else: #This is a function declaration (We will use the code block later
                        statements.append(types.Statement("Function Declaration", statement, currentLine))
                        currentLine += 1
                    #End else

                    i = j
                        
                #End else
                
            #End if

            elif symbols[j].value is "(": #This is a function pointer
                while symbols[j].value is not ";" and symbols[j].value is not "=":
                    statement.append(" ", symbols[j].value)
                    j += 1
                #End while

                statements.append(types.Statement("Function Pointer Declaration", statement + ";", currentLine))
                currentLine += 1

                if symbols[j].value is "=": #The pointer is initialized in the same statement
                    statement = symbols[i].value + " =" #Using i for two things at once
                    j += 1

                    while symbols[j].value is not ";":
                        statement.append(" " + symbols[j].value)
                        j += 1
                    #End while

                    statements.append(types.Statement("Function Pointer Initialization", statement, currentLine))
                    currentLine += 1
                    i = j
                #End if
                
            #End elif
            
        #End elif

        elif symbols[i].kind is "$i": #This is a reassignment, function call, or struct member access call
            statement = ""
            kind = ""
            j = 1

            while symbols[i + j].value is not "=":
                if symbols[i + j].value is ";":
                    kind = "Function Call"
                    break
                j += 1
            #End while
            
            if kind is "":
                kind = "Variable Reassignment"
            #End if
            
            while symbols[i].value is not ";":
                statement.append(symbols[i].value)
                i += 1
            #End while

            statement.append(";")
            statements.append(types.Statement(kind, statement, currentLine))
            currentLine += 1
        #end elif

        elif symbols[i].kind is "$l": #This is the beginning of a loop
            statement = ""
            
            if symbols[i].value is not "do": #Because "do" takes no arguments, but while does
                statement = symbols[i].value
                i += 1
                statement.append(" " + symbols[i].value) #The left parenthesis
                i += 1

                lcount = 1

                while lcount is not 0:
                    statement.append(" " + symbols[i].value)
                    if symbols[i].value is "(":
                        lcount += 1
                    #End if
                        
                    elif symbols[i].value is ")":
                        lcount -= 1
                    #End elif
                        
                    i += 1
                #End while
            #End if
            
            else: #If it is a do-while loop
                statement = symbols[i].value
            #End else
                
            statements.append(types.Statement("Loop Declaration", statement, currentLine))
            currentLine += 1
        #end elif

        elif symbols[i].kind is "$c": #This is a conditional branching statement
            if symbols[i].value is "case":
                statement = symbols[i : i + 2].value.join(" ")
                i += 2
            #End if

            elif symbols[i].value is "else":
                statement = symbols[i].value
            #End elif

            else:
                statement = symbols[i].value
                i += 1
                statement.append(" " + symbols[i].value)
                i += 1

                lcount = 1

                while lcount is not 0:
                    statement.append(" " + symbols[i].value)
                    if symbols[i].value is "(":
                        lcount += 1
                    #End if
                        
                    elif symbols[i].value is ")":
                        lcount -= 1
                    #End elif
                        
                    i += 1
                #End while

            #End else
                
            statements.append(types.Statement("Conditional Branching Statement", statement, currentLine))

            currentLine += 1
        #end elif

        elif symbols[i].kind is "$f": #This is a flow control statement
            statement = symbols[i].value
            
            if symbols[i].value is "goto" or symbols[i].value is "return":
                i += 1
                while symbols[i].value is not ";":
                    statement.append(" " + symbols[i].value)
                    i += 1
                #End while

                statement.append(symbols[i].value)
            #End if
            
            else:
                i += 1
                statement.append(symbols[i].value)
            #End else

            statements.append(types.Statement("Flow Control Statement", statement, currentLine))
            currentLine += 1
        #end elif

        elif symbols[i].kind is "$t": #This is a type declaration
            statement = ""
            
            if symbols[i].value is "typedef":
                statement.append(symbols[i].value)
                i += 1
            #End if

            while symbols[i].value is not "}":
                statement.append(" " + symbols[i].value)
                i += 1
            #End while

            while symbols[i].value is not ";":
                statement.append(" " + symbols[i].value)
                i += 1
            #End while

            statement.append(";")
            statements.append(types.Statement("Type Definition", statement, currentLine))
            currentLine += 1
        #end elif

        elif symbols[i].value is "{":
            statement = symbols[i].value
            i += 1
            lbrace = 1

            while lbrace > 0:
                statement.append(symbols[i].value)
                if symbols[i].value is "{":
                    lbrace += 1
                #End if

                elif symbols[i].value is "}":
                    lbrace -= 1
                #End elif

                i += 1
            #End while

            statements.append(types.Statement("Code block", statement, currentLine))
            currentLine += 1
        #End elif

        else: #If nothing else matches, just scan to the next semicolon and hope it works
            statement = symbols[i].value
            i += 1
            
            while symbols[i].value is not ";":
                statement.append(" " + symbols[i].value)
                i += 1
            #End while

            statement.append(";")
            statements.append(types.Statement("Miscellanious (See plaintext)", statement, currentLine))
            currentLine += 1
        
        i += 1
    #End while
#End def parse(symbols):

