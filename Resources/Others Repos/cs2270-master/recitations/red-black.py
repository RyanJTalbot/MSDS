RED = 0
BLACK = 1

class red_black_node:
    color = BLACK
    parent = None
    left = None
    right = None
    value = 0

def sibling(n):
    if n == n.parent.left:
        return n.parent.right
    else:
        return n.parent.left

# returns grandparent of node, or None if not available
def grampa(n):
    if n is not None and n.parent is not None:
        return n.parent.parent
    else:
        return None

# return the uncle node of n (parent's sibling).
def uncle(n):
    g = grampa(n)
    if g is None:
        return None
    if n.parent == g.left:
        return g.right
    else:
        return g.left


