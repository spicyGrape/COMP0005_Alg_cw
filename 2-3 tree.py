class Node23 :
    def __init__(self,is_leaf=True):
        self.keys = [] #maximum 2
        self.children = [] #maximum 3
        self.is_leaf = is_leaf
class Tree23 :
    def __init__(self):
        self.root = None
    def search(self,key):
        pass
    def insert(self,key):
        if self.root is None:
            self.root = Node23(is_leaf=True)
            self.root.keys.append(key)
            return
        promotion = self.insert_recursively(self.root,key)
        if promotion is not None: # deal with the root
            mid_key, new_left, new_right = promotion
            new_root = Node23(is_leaf=False)
            new_root.keys.append(mid_key)
            new_root.children = [new_left, new_right]
            self.root = new_root
    def insert_recursively(self,node,key):
        if node.is_leaf :
            self.insert_to_left(node,key)
            if len(node.keys) > 2:
                return self.split_leaf(node)
            return None
        else :
            children_index = self.find_children_index(node,key)
            promotion = self.insert_recursively(node.children[children_index],key)
            if promotion is not None: #deal with the parent node in each lays
                mid_key,new_left,new_right = promotion
                self.merge(node,mid_key,new_left,new_right)
                if len(node.keys) > 2:
                    return self.split_internal(node)
            return None
    def split_leaf(self,node):
        mid_key = node.keys[1]
        new_left = Node23(is_leaf=True)
        new_left.keys.append(node.keys[0])
        new_right = Node23(is_leaf=True)
        new_right.keys.append(node.keys[2])
        return mid_key,new_left,new_right
    def split_internal(self,node):
        mid_key = node.keys.pop(1)
        new_left = Node23(is_leaf=False)
        new_left.keys.append(node.keys[0])
        new_left.children =node.children[0:2]
        new_right = Node23(is_leaf=False)
        new_right.keys.append(node.keys[1])
        new_right.children =node.children[2:]
        return mid_key,new_left,new_right
    def merge(self,node,mid_key,new_left,new_right):
        idx = self.find_children_index(node,mid_key)
        node.keys.insert(idx,mid_key)
        node.children[idx] =new_left
        node.children.insert(idx + 1, new_right)
    def insert_to_left(self,node,key): #insert the key to the left
        idx = 0
        while idx < len(node.keys) and key > node.keys[idx]:
            idx += 1
        node.keys.insert(idx,key)
    def find_children_index(self,node,key):
        idx = 0
        while idx < len(node.keys) and key > node.keys[idx]:
            idx += 1
        return idx
    def print_tree(self,node, level=0):
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
    tree.print_tree(tree.root)
