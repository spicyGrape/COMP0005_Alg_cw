class Node23:
    def __init__(self, is_leaf=True):
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf
class Tree23:
    def __init__(self):
        self.root = None
    def search(self, key):
        if self.root is None:
            return False
        else:
            return self.search_recursively(self.root,key)

    def insert(self, key):
        if self.root is None:
            self.root = Node23(is_leaf=True)
            self.root.keys.append(key)
            return True
        success, promotion = self.insert_recursively(self.root, key)
        if not success:
            return False
        if promotion is not None: # deal with the root
            mid_key, new_left, new_right = promotion
            new_root = Node23(is_leaf=False)
            new_root.keys.append(mid_key)
            new_root.children = [new_left, new_right]
            self.root = new_root
        return True

    def insert_recursively(self, node, key):
        if key in node.keys:
            return (False, None)

        if node.is_leaf :
            self.insert_to_left(node, key)
            if len(node.keys) > 2:
                promotion = self.split_leaf(node)
                return (True, promotion)
            return (True, None)
        else :
            children_index = self.find_children_index(node,key)
            success, promotion = self.insert_recursively(node.children[children_index],key)
            if not success:
                return (False, None)
            if promotion is not None: #deal with the parent node in each lays
                mid_key,new_left,new_right = promotion
                self.merge(node,mid_key,new_left,new_right)
                if len(node.keys) > 2:
                    promotion_internal = self.split_internal(node)
                    return (True, promotion_internal)
            return (True, None)

    def split_leaf(self, node):
        mid_key = node.keys[1]
        new_left = Node23(is_leaf=True)
        new_left.keys.append(node.keys[0])
        new_right = Node23(is_leaf=True)
        new_right.keys.append(node.keys[2])
        return mid_key,new_left,new_right

    def split_internal(self, node):
        mid_key = node.keys.pop(1)
        new_left = Node23(is_leaf=False)
        new_left.keys.append(node.keys[0])
        new_left.children =node.children[0:2]
        new_right = Node23(is_leaf=False)
        new_right.keys.append(node.keys[1])
        new_right.children =node.children[2:]
        return mid_key,new_left,new_right

    def merge(self, node, mid_key, new_left, new_right):
        idx = self.find_children_index(node, mid_key)
        node.keys.insert(idx, mid_key)
        node.children[idx] =new_left
        node.children.insert(idx + 1, new_right)

    def insert_to_left(self, node, key): #insert the key to the left
        idx = 0
        while idx < len(node.keys) and key > node.keys[idx]:
            idx += 1
        node.keys.insert(idx, key)

    def find_children_index(self, node, key):
        idx = 0
        while idx < len(node.keys) and key > node.keys[idx]:
            idx += 1
        return idx

    def search_recursively(self, node, key):
         n = len(node.keys)
         for idx in range(n):
            if node.keys[idx] == key:
                return True
         if node.is_leaf :
            return False
         else:
            children_index = self.find_children_index(node, key)
            return self.search_recursively(node.children[children_index],key)

    def print_tree(self, node, level=0):
        if node is None:
            return
        print(f"Level {level}: {node.keys}")
        if not node.is_leaf:
            for child in node.children:
                self.print_tree(child, level + 1)

if __name__ == '__main__':
    tree = Tree23()
    keys = [7, 3, 10, 1, 5, 8, 2, 4, 6, 9]
    for k in keys:
        tree.insert(k)
    tree.print_tree(tree.root,0)
    a = tree.search(8)
    print(a)
    b = tree.search(11)
    print(b)
    k = tree.insert(10)
    print(k)
