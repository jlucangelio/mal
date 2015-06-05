import maltypes

def pr_str(node):
    if type(node) == maltypes.Symbol:
        return str(node)
    elif type(node) == list:
        return "(" + " ".join([pr_str(c) for c in node]) + ")"
    elif type(node) == int:
        return str(node)
