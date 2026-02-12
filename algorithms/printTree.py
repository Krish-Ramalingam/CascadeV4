def printTree(node, level=0): 
    if node is not None: 
        printTree(node.right, level + 1) 
        print(' ' * 4 * level + '-> ' + str(node.token))
