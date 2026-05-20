from collections import deque
class MyStack:
    def __init__(self):
        self.queue = deque()
    def push(self, x):
        self.queue.append(x)
        for _ in range(len(self.queue)-1):
            self.queue.append(self.queue.popleft())
    def pop(self):
        return self.queue.popleft()
    def top(self):
        return self.queue[0]
    def empty(self):
        return len(self.queue) == 0
