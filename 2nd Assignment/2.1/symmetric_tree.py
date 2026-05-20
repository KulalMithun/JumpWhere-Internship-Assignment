class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_symmetric(node1, node2):
    if node1 is None and node2 is None:
        return True
    if (node1 is None) or (node2 is None) or node1.val != node2.val:
        return False
    return is_symmetric(node1.left, node2.right) and is_symmetric(node1.right, node2.left)

def is_tree_symmetric(root):
    if root is None:
        return True
    return is_symmetric(root.left, root.right)
if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(2)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(4)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(3)
    print(is_tree_symmetric(root))
