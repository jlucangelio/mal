def pr_str(node):
    if type(node) == str:
        return node
    elif type(node) == list:
        return "(" + " ".join([pr_str(c) for c in node]) + ")"
    elif type(node) == int:
        return str(node)
