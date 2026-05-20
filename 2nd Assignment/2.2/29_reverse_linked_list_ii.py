class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
def reverseBetween(head, left, right):
    if left == right:
        return head
    dummy = ListNode(0, head)
    prev_node = dummy
    for _ in range(left-1):
        prev_node = prev_node.next
    reverse_start = prev_node.next
    for _ in range(right-left):
        next_node = reverse_start.next
        reverse_start.next = next_node.next
        next_node.next = prev_node.next
        prev_node.next = next_node
    return dummy.next
