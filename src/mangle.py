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

import parser

class Function:
    func_id = 0
    statements = []
    subdivisions = []

    def __init__(self, statements):
        self.statements = statements

class Subdivision:
    sub_id = 0
    location = 0
    lines = []

    def __init__(self, lines):
        self.lines = lines

#Will be implemented later
def mangle_easy(statements, key):
    pass
#End mangle_easy(statements)

"""
Overview:
1) Take all variables and type definitions and make them global
2) Make sub-lists from functions
3) Split each sub-list into sub-sub-lists of two statements each
4) Make the key the random seed and assign each sub-list a number using the pseudo-random number generator
5) Assign each sub-sub-list a number from the pseudo-random number generator
6) Determine the place in the switch statement by multiplying the sub-list number and the sub-sub-list number
7) In the rare case of a collision, keep adding one until there is no longer a collision
8) Link all the sub-sub-lists using a global index and calling the same function
9) Link all the sub-lists by replacing the function calls similarly
10) Print it all into a single switch statement in one function
"""
def mangle_hard(statements, key):
    #Various lists for use later

    variables = []

    functions = []

    newStatements = []
    
    #Step 1

    for statement in statements:
        if statement.kind in ["Variable Declaration", "Function Pointer Declaration", "Type Definition"]:
            variables.append(statement)
        #End if

    #End for
    
    #End Step 1

    #Step 2

    for statement in statements

    #End Step 2
    
#End mangle_hard(statements):
