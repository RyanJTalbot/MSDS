#
# binary_search_tree.py
#

class bt_node:
    data = 0
    left = None
    right = None

class BinarySearchTree:

    def __init__(self):
        """
        Please use 'root_node' to refer to your topmost entry. This is
        needed for unit testing. It is a bt_node object.
        """
        self.root_node = None

    def init_node(self, data):
        """
        Create and return a bt_node object that has been initialized
        with the given data and two None children.
        """
        pass

    def insert(self, new_node):
        """
        Insert the new_node into the tree at the correct location.
        """
        pass

    def insert_data(self, data):
        """
        Insert a new node that contains the given data into the tree
        at the correct location.
        """
        pass

    def remove(self, data):
        """
        Removes a node from the tree whose data value is the same as
        the argument.
        """
        pass

    def contains(self, data):
        """
        Return True or False depending on if this tree contains a node
        with the supplied data.
        """
        pass

    def get_node(self, data):
        """
        If the tree contains a node with the supplied data, return
        it. Otherwise return None.
        """
        pass

    def size(self):
        """
        Return the size of this tree. If it is empty this returns 0.
        """
        pass

    def to_array(self):
        """
        Create and fill a list with the data contained in this
        tree. The elements of the returned list must be in the same
        order as they are found during an inorder traversal, which
        means the numbers should be in non-decreasing order.
        """
        pass
