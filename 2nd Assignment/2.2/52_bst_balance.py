class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
def balanceBST(root):
    def inorder(node, vals):
        if not node:
            return
        inorder(node.left, vals)
        vals.append(node.val)
        inorder(node.right, vals)
    def build(left, right):
        if left > right:
            return None
        mid = (left+right)//2
        node = TreeNode(vals[mid])
        node.left = build(left, mid-1)
        node.right = build(mid+1, right)
        return node
    vals = []
    inorder(root, vals)
    return build(0, len(vals)-1)
