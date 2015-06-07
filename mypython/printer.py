import maltypes

def pr_str(node):
    if isinstance(node, maltypes.Type):
        return str(node)
    elif type(node) == list:
        return "(" + " ".join([pr_str(c) for c in node]) + ")"
    elif type(node) == int:
        return str(node)
    elif callable(node):
        # return node.func_name
        return "#<function>"
    elif node == None:
        return "nil"
    elif node == True:
        return "true"
    elif node == False:
        return "false"
    else:
        raise Exception("Invalid type")
