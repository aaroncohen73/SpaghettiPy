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

import random

import parser

class Function:
    func_id = 0
    declaration = None
    subdivisions = []

    def __init__(self, declaration, subdivisions):
        self.declaration = declaration
        self.subdivisions = subdivisions
#End class Function
        
class Loop:
    pass
#End class Loop
        
class Subdivision:
    sub_id = 0
    location = 0
    next_sub = 0
    lines = []

    def __init__(self, lines):
        self.lines = lines
#End class Subdivision
        
"""
Overview:
1) Take all variables and type definitions and make them global
2) Make the key the random seed and assign each sub-list a number using the pseudo-random number generator
3) Give each function a number from the generator
4) "Straighten" the loops and conditionals by turning them into a series of subdivisions linked by pseudo-random numbers
5) Turn all other statements into subdivisions of no more than two lines each, and link them
6) Determine each subdivision's final place in the switch statement by multiplying their ID with that of their function
7) In the rare case of a collision, keep adding one until there is no longer a collision
8) Print it all into a single switch statement in one function
"""
def mangle_hard(statements, key):
    #Various lists for use later

    variables = []

    functions = []

    newStatements = []
    
    #Step 1

    for statement in statements:
        if statement.kind in ["Variable Declaration", "Function Pointer Declaration", "Type Definition", "Function Prototype"]:
            variables.append(statement)
        #End if

    #End for
    
    #End Step 1

    #Steps 2 and 3

    i = 0
    while i < len(statements):
        if statements[i].kind == "Function Declaration":
            declaration = statements[i].value
            funcStatements = []
            lbrace = 1
            while lbrace > 0:
                i += 1
                
                if statements[i].kind == "Begin Code Block":
                    lbrace += 1
                #End if

                elif statements[i].kind == "End Code Block":
                    lbrace -= 1
                #End elif

                else:
                    funcStatements.append(statements[i])
                #End else

            #End while

            subdivisions = []
            lines = []
            
            for i in xrange(0, len(funcStatements), 2):
                if i == len(funcStatements) - 1:
                    lines = [funcStatements[i]]
                #End if

                else:
                    lines = [funcStatments[i], funcStatements[i + 1]]
                #End else

                subs.append(Subdivision(lines))
            #End for

            functions.append(Function(declaration, subdivisions))

        #End if

    #End while

    #End Steps 2 and 3

    #Steps 4 and 5

    random.seed(key)

    for function in functions:
        function.func_id = random.randint(-2147483647, 2147483647)

        for subdivision in function.subdivisions:
            subdivision.sub_id = random.randint(-2147483647, 2147483647)
        #End for

    #End for

    #End Steps 4 and 5
    
#End mangle_hard(statements):
