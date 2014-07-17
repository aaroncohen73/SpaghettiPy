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
from types import Statement

#Refer to Identifier table in lexer.py
statementPatterns = {"Variable Initialization":"%v+\s%i"}

def parse(symbols):
"""
Parses a list of symbols and returns a list of statements
"""
    statements = []
    i = 0
    currentLine = 0;

    while symbols[i].kind is not "EOF":
        if symbols[i].kind is "Macro":
            statements.append("Macro", symbols[i].value, currentLine)
            currentLine += 1

        

        i += 1
   
    
