class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
def deleteNode(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        min_larger = root.right
        while min_larger.left:
            min_larger = min_larger.left
        root.val = min_larger.val
        root.right = deleteNode(root.right, min_larger.val)
    return root
