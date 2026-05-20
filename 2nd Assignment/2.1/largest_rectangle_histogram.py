def largest_rectangle(heights):
    heights = [-1]+heights+[-1]
    max_area = 0
    stack = [(0, -1)]
    for i in range(1, len(heights)):
        start = i
        while stack[-1][1] > heights[i]:
            top_index, top_height = stack.pop()
            max_area = max(max_area, top_height*(i-top_index))
            start = top_index
        stack.append((start, heights[i]))
    return max_area
if __name__ == "__main__":
    print(largest_rectangle([2, 1, 5, 6, 2, 3]))
