def sortStack(stack):
    def sort_helper(stack):
        if len(stack) == 0:
            return
        top = stack.pop()
        sort_helper(stack)
        insert_sorted(stack, top)
    def insert_sorted(stack, value):
        if len(stack) == 0 or stack[-1] <= value:
            stack.append(value)
        else:
            top = stack.pop()
            insert_sorted(stack, value)
            stack.append(top)
    sort_helper(stack)
    return stack
