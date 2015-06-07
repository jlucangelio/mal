import maltypes

def pr_str(node, print_readably=False):
    if isinstance(node, maltypes.Type):
        return str(node)
    elif type(node) == list:
        return "(" + " ".join([pr_str(c, print_readably) for c in node]) + ")"
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
    elif type(node) == str:
        if print_readably:
            return '"%s"' % node.replace('"', r'\"')
        else:
            return node
    else:
        raise Exception("Invalid type")
