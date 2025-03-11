class NodeAVL:
    def __init__(self, key, parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent
        self.height = 1

class TreeAVL:
    def __init__(self):
        self.root = None

    def getHeight(self, node):
        return node.height if node else 0

    def getBalanceFactor(self, node):
        if not node:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)

    def updateHeight(self, node):
        if node:
            node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))

    def leftRotate(self, node):

        rightChild = node.right
        if not rightChild:
            return node

        T2 = rightChild.left

        rightChild.left = node
        node.right = T2

        rightChild.parent = node.parent
        node.parent = rightChild
        if T2:
            T2.parent = node

        if rightChild.parent is None:
            self.root = rightChild
        else:
            if rightChild.parent.left == node:
                rightChild.parent.left = rightChild
            else:
                rightChild.parent.right = rightChild

        self.updateHeight(node)
        self.updateHeight(rightChild)
        return rightChild

    def rightRotate(self, node):
        leftChild = node.left
        if not leftChild:
            return node

        T2 = leftChild.right

        leftChild.right = node
        node.left = T2

        leftChild.parent = node.parent
        node.parent = leftChild
        if T2:
            T2.parent = node

        if leftChild.parent is None:
            self.root = leftChild
        else:
            if leftChild.parent.left == node:
                leftChild.parent.left = leftChild
            else:
                leftChild.parent.right = leftChild

        self.updateHeight(node)
        self.updateHeight(leftChild)
        return leftChild

    def insert(self, key):
        self.root = self._insert(self.root, key, parent=None)

    def _insert(self, node, key, parent):
        if not node:
            return NodeAVL(key, parent)
        if key < node.key:
            node.left = self._insert(node.left, key, node)
        elif key > node.key:
            node.right = self._insert(node.right, key, node)
        else:
            # Duplicate keys are not allowed
            return node

        self.updateHeight(node)
        balance = self.getBalanceFactor(node)

        # Left Left Case
        if balance > 1 and node.left and key < node.left.key:
            return self.rightRotate(node)
        # Right Right Case
        if balance < -1 and node.right and key > node.right.key:
            return self.leftRotate(node)
        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)
        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)

        return node

    def search(self, key):
        node = self.root
        while node:
            if node.key == key:
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return False

    def print_tree(self,node, level=0):
        if node is None:
            return
        print(f"Level {level}: {node.key}")
        self.print_tree(node.right, level + 1)
        self.print_tree(node.left, level + 1)

if __name__ == "__main__":
    avl = TreeAVL()
    keys = [7, 12, 3, 10, 1, 13, 5, 11, 8, 2, 14, 4, 6, 9]
    for k in keys:
        print("Inserting ", k)
        avl.insert(k)
        avl.print_tree(avl.root,0)

    found = avl.search(9)
    if found:
        print(f"Found key: {found.key}")
    else:
        print("Key not found.")
