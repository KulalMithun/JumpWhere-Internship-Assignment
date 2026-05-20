class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
def findTarget(root, k):
    def inorder(node, vals):
        if not node:
            return
        inorder(node.left, vals)
        vals.append(node.val)
        inorder(node.right, vals)
    vals = []
    inorder(root, vals)
    left, right = 0, len(vals)-1
    while left < right:
        total = vals[left] + vals[right]
        if total == k:
            return True
        elif total < k:
            left += 1
        else:
            right -= 1
    return False
