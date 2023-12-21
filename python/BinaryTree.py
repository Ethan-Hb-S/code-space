class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self) -> None:
        self.top = None
    
    def transform(self, list):
        arr = sorted(list)
        top = build_binary_tree(arr, 0, len(arr)-1)
        self.top = top
    
    def traverse(self):
        self.show(self.top)

    def show(self, node: Node):
        if node == None:
            return
        self.show(node.left)
        print(node.value)
        self.show(node.right)

def build_binary_tree(arr, min, max) -> Node:
    if min > max:
        return None
    mid = (max + min + 1) // 2
    top = Node(arr[mid])

    if min == max:
        return top
    else:
        top.left = build_binary_tree(arr, min, mid-1)
        top.right = build_binary_tree(arr, mid+1, max)
        return top