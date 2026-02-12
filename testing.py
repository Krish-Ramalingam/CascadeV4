from servantClasses import lineLexer as l
from algorithms import dijkstra as d
from algorithms import evalpostfix as e

tstream = (l.genTokStream())
for x in tstream:
    print(x)


#var = tstream[0][1]
#tstream = tstream[2:]
#postTStream = d.dijkstraShuntingYard(tstream)
#print(postTStream)
#evaledTStream = e.evalPostExpr(postTStream)
#print(var, "=", evaledTStream)