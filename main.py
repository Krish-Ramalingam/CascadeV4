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

with open("devlog.txt", "w") as f:
    f.write("")

def writeToDevLog(logs):
    with open("devlog.info", "a") as f:
        for log in logs:
            if type(log[1]) == str or type(log[1]) == int or type(log[1]) == float:
                f.write(log[0] + ": " + str(log[1]) + "\n")
            else:
                f.write(log[0] + "\n")
            
#lexing
lexer = lxr.Lexer()
token_stream = lexer.lexFile("inputfiles/" + x)
print(token_stream)
print("\n")
writeToDevLog(token_stream)

#parsing
parser = psr.ParserNodes(token_stream)
ast_nodes = parser.parse_program()
print(ast_nodes)
print("\n")

#interpreting
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
    