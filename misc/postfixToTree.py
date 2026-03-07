#postExpr = [("int", 3), ("int", 2), ("int", 5), ("+", None), ("*", None)]

def getType(tok): 
    if tok[0] in ["var", "int", "float"]: 
        return "data"
    else:
        return "op"

class Node: 
    def __init__(self, token): 
        self.token = token
        self.left = None
        self.right = None


def postFixToTree(tokenisedExpr):
    ramQueue = []
    for t in tokenisedExpr: 
        if getType(t) == "data":
            node = Node(t)
            ramQueue.append(node)
        else:
            node = Node(t)
            node.right = ramQueue[-1]
            node.left = ramQueue[-2]
            ramQueue.pop()
            ramQueue.pop()
            ramQueue.append(node)
    return ramQueue[0]
    
def printTree(node, level=0): 
    if node is not None: 
        printTree(node.right, level + 1) 
        print(' ' * 4 * level + '-> ' + str(node.token))
        printTree(node.left, level + 1)
        
#printTree(postFixToTree(postExpr))
