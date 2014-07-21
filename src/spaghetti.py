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

import sys

import lexer
import parser

def main(argc, argv):
    if argc != 3:
        print("Usage: %s <File Path> [Key]" % argv[0])
        return
    #End if
    
    sourceFile = open(argv[1], "r")
    source = sourceFile.read()
    statements = parser.parse(lexer.lex(source))

    print(statements[0].plaintext)

#End def main(argc, argv)

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
#End if
