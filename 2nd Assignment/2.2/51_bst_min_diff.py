class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
def getMinimumDifference(root):
    prev = [None]
    min_diff = [float('inf')]
    def inorder(node):
        if not node:
            return
        inorder(node.left)
        if prev[0] is not None:
            min_diff[0] = min(min_diff[0], node.val-prev[0])
        prev[0] = node.val
        inorder(node.right)
    inorder(root)
    return min_diff[0]
