class BTreeNode:
    def __init__(self, keys=None, children=None, parent=None):

        self.keys = keys if keys is not None else []
        self.children = children if children is not None else []
        self.parent = parent

    def get_keys(self):
        return self.keys

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent


class BTree(AbstractSearchInterface):
    """
    max_keys refers to the maximum possible keys held by a node 
    For this BTree implementation we set max_keys arbitrary to 4 by default, however this can be overriden"
    """
    def __init__(self, max_keys=4):
        self.root_node = BTreeNode()
        self.max_keys = max_keys

    def insertElement(self, element):
        inserted = False
        # No need to insert the element if its already present
        if self.searchElement(element):
            return inserted
        self.insert(element, self.root_node)
        return True

    def splitNode(self, node):

        node_keys = node.get_keys()
        node_children = node.get_children()
        mid_idx = len(node_keys) // 2

        left_child_keys = node_keys[:mid_idx]
        median_key = node_keys[mid_idx]
        right_child_keys = node_keys[mid_idx + 1:]

        left_children = node_children[:len(node_children) // 2] if node_children else []
        right_children = node_children[len(node_children) // 2:] if node_children else []

        left_child = BTreeNode(keys=left_child_keys, children=left_children, parent=None)
        right_child = BTreeNode(keys=right_child_keys, children=right_children, parent=None)

        for child in left_child.get_children():
            child.parent = left_child
        for child in right_child.get_children():
            child.parent = right_child

        #Case 1 : node is root node, thus we create a new node to become the parent node and thus the new root node
        if node == self.root_node:
            new_root = BTreeNode(keys=[median_key], children=[left_child, right_child])
            left_child.parent = new_root
            right_child.parent = new_root
            self.root_node = new_root
            return

        # Case 2: Non-root node, we insert median key into parent node and append the new nodes into parent node's children
        parent = node.get_parent()
        parent_keys = parent.get_keys()
        parent_children = parent.get_children()

        idx = 0
        while idx < len(parent_keys) and parent_keys[idx] < median_key:
            idx += 1

        parent_keys.insert(idx, median_key)

        # Remove the pointer to the split node and insert the two new children.
        parent_children.pop(idx)
        left_child.parent = parent
        right_child.parent = parent
        parent_children.insert(idx, left_child)
        parent_children.insert(idx + 1, right_child)

        # Recursively split the parent if needed.
        if len(parent_keys) >= self.max_keys:
            self.splitNode(parent)

    def insert(self, element, node):
        node_children = node.get_children()
        node_keys = node.get_keys()

        #Leaf Node, hence, we simply insert element in sorted order and split if necessary
        if not node_children:  
            idx = 0
            while idx < len(node_keys) and node_keys[idx] < element:
                idx += 1
            node_keys.insert(idx, element)
            if len(node_keys) >= self.max_keys:
                self.splitNode(node)
            return

        #Otherwise: We traverse the B-Tree to find the appropriate Leaf Node
        idx = 0
        while idx < len(node_keys) and node_keys[idx] < element:
            idx += 1
        self.insert(element, node_children[idx])

    def searchElement(self, element):
        return self.search(element, self.root_node)


    def search(self, element, node):

        #Case 1: Element is in current node's keys, we return true immediately
        node_keys = node.get_keys()
        if element in node_keys:
            return True

        #Case 2: Element is not in current node's keys is a leaf node, hence we return false as there are no more children
        node_children = node.get_children()
        if not node_children:
            return False

        #We recursively call search() on the appropriate child node
        idx = 0
        while idx < len(node_keys):
            if node_keys[idx] > element:
                break
            idx += 1

        if idx >= len(node_children):
            return False

        return self.search(element, node_children[idx])
