#
#    Copyright (C) 2014 Aaron Cohen                                                                                              
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

import random

import parser

#End imports

class Subdivision(object):
    statements = []
    subID = -1
    nextSub = None
#End class Subdivision

class Block(object):
    declaration = None
    statements = []
    subdivisions = []
    children = []
    parent = None
    level = -1
    blockID = -1
    beginning = 0
    end = 0
#End class Block

def findBlocks(statements, currentStatement, currentLevel):
    """
Creates a heirarchy of Blocks out of a list of Statements
    """
    
    block = Block()
    block.level = currentLevel
    block.beginning = currentStatement

    if currentLevel > 0:
        block.declaration = statements[currentStatement - 2]
    #End if
    
    while True:
        if statements[currentStatement] == "Begin Code Block":
            block.children.append(findBlocks(statements, currentStatement + 1, currentLevel + 1))
            block.children[-1].parent = block
            statements.append(Statement("BREAK", "Break at statement " + str(currentStatement), statements[currentStatement].line))
            currentStatement = block.children[-1].end + 1
        #End if

        elif statements[currentStatement] == "End Code Block" or currentStatement == len(statements):
            block.end = currentStatement
            return block
        #End elif

        block.statements.append(statements[currentStatement++])
    #End while
        
#End findBlocks(statements, currentStatement, currentLevel, blocksSoFar):

def subdivide(parent):
    """
Creates Subdivisions out of a heirarchy of Blocks
    """
    
    if len(parent.children) > 0:
        for child in parent.children:
            subdivide(child)
        #End for

    #End if

    for i in range(0, len(parent.statements), 2):
        subdivision = Subdivision
        subdivision.statements.append(parent.statements[i])
        if i != len(parent.statements) - 1:
            subdivision.statements.append(parent.statements[i + 1])
        #End if
        
        parent.subvisions.append(subdivision)
        if len(parent.subdivisions) > 1:
            parent.subdivisions[-2].nextSub = parent.subdivisions[-1]
        #End if

    #End for
    
#End subdivide(parent)

def link(parent):
    """
Links subdivided Blocks together
    """

    
#End link(parent)

"""
Overview:
1) Make the key the random seed
2) Put all variable declarations and function pointers into a new list, and remove prototypes
3) Turn the statements into blocks of code
4) Turn the code inside the blocks into subdivisions of two statements each
5) Generate the boilerplate code to make constructs such as conditionals work.
6) Give each subdivision and block a random ID
7) Check for collisions (NOTE: Boilerplate can take up several IDs)
8) Link each subdivision and block to the next
9) Turn the boilerplate for the blocks into regular subdivisions and link those appropriately
10) Rename all the variables after their original scope (Ex: variablename__global or variablename__function1__for__2)
11) Give all external functions their own IDs and make calls to them subdivisions
12) Change all function pointers to their IDs
"""
def mangle(statements, key):
    """
Mangles a list of Statements according to the above algorithm
    """

    random.seed(key)

    variables = []
    functionPointers = []
    
    for i in range(0, len(statements)):
        if statements[i].kind == "Variable Declaration":
            variables.append(statements.pop(i))
        #End if

        elif statements[i].kind == "Function Pointer Declaration":
            functionPointers.append(statements.pop(i))
        #End elif

        elif statements[i].kind == "Function Prototype":
            statements.remove(i)
        #End elif

    #End for

    globalBlock = findBlocks(statements, 0, 0)

    subdivide(globalBlock)

#End mangle(statements, key):
