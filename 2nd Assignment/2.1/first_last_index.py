def find_first_last(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            start = i
            while i+1 < len(arr) and arr[i+1] == target:
                i += 1
            return [start, i]
    return [-1, -1]
if __name__ == "__main__":
    print(find_first_last([5, 7, 7, 8, 8, 10], 8))
