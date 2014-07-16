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

def parse(source):
"""
Takes source code and makes it easier to parse (i.e. separates each statement onto its own line, sets marks to tell the mangler the location of things

Re-organizations that this function does:

//__BEGIN_FUNCTION__
return type
function()
{
    Statement;
}
//__END_FUNCTION__

//__BEGIN_FUNCTION_PROTOTYPE__
return type
function();
//__END_FUNCTION_PROTOTYPE__

//__BEGIN_STRUCT__
struct
str
{
    Element;
}
//__END_STRUCT__

//__BEGIN_TYPEDEF_STRUCT__
typedef struct
{
    Element;
}
name_t;
//__END_TYPEDEF_STRUCT__

//__BEGIN_WHILE_LOOP__
while(condition)
{
    Statement;
}
//__END_WHILE_LOOP__

//__BEGIN_DO_WHILE_LOOP__
do
{
    Statement;
}
while(condition)
//__END_DO_WHILE_LOOP__

//__BEGIN_FOR_LOOP__
for(initializer, condition, statement)
{
    Statement;
}
//__END_FOR_LOOP__

...
{
    //__BEGIN_LOCAL_VARIABLE__
    variable type var;
    //__END_LOCAL_VARIABLE
    
    //__BEGIN_LOCAL_VARIABLE___
    variable type var2;
    //__END_LOCAL_VARIABLE__
}

"""

    
