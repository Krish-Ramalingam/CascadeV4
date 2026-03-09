import os
from os import listdir
from os.path import isfile, join
from maincode.core import lexer as lxr
from maincode.core import parser as psr
from maincode.core import interpreter as itp

onlyfiles = [f for f in listdir("inputfiles") if isfile(join("inputfiles", f))]
cscfiles = [f for f in onlyfiles if f.endswith(".csc")]

def select_file():
    if len(cscfiles) == 0:
        print("No input files found in the inputfiles directory. Run the program again after adding an input file to the inputfiles directory.")
    elif len(cscfiles) > 1:
        desired_file = input("Multiple input files found in the inputfiles directory. Which file would you like to use?" + "\n" + "\n".join(cscfiles) + "\n")
        if desired_file not in cscfiles:
            print("Invalid file name. Please select a valid file.")
            select_file()
        else:
            return desired_file
    elif len(cscfiles) == 1:
        desired_file = cscfiles[0]
        return desired_file
    
x = select_file()
os.system('cls')

lexer = lxr.Lexer()
token_stream = lexer.lexFile("inputfiles/" + x)
parser = psr.ParserNodes(token_stream)
ast_nodes = parser.parse_program()
interpreter = itp.Interpreter()
interpreter.exec_nodes(ast_nodes)


"""
lexer = lxr.Lexer()
token_stream = lexer.lexFile(file_contents)
parser = psr.ParserNodes(token_stream)
ast_nodes = parser.parse_program()
interpreter = itp.Interpreter()
interpreter.exec_nodes(ast_nodes)
"""
    