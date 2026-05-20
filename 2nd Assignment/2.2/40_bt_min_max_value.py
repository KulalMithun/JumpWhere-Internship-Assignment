class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
def findMin(root):
    if not root:
        return None
    min_val = root.val
    if root.left:
        min_val = min(min_val, findMin(root.left))
    if root.right:
        min_val = min(min_val, findMin(root.right))
    return min_val
def findMax(root):
    if not root:
        return None
    max_val = root.val
    if root.left:
        max_val = max(max_val, findMax(root.left))
    if root.right:
        max_val = max(max_val, findMax(root.right))
    return max_val
