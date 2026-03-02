from servantClasses import lineLexer as l
from algorithms import dijkstra as d
from algorithms import evalpostfix as e
from finalcode import parser as p





tstream = (l.genTokStream())
parser = p.ParserNodes(tstream)
ast_nodes = parser.parse_program()

for node in ast_nodes:
    print(node)
    

#var = tstream[0][1]
#tstream = tstream[2:]
#postTStream = d.dijkstraShuntingYard(tstream)
#print(postTStream)
#evaledTStream = e.evalPostExpr(postTStream)
#print(var, "=", evaledTStream)