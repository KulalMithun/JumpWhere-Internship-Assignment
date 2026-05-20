def minimumAbsoluteDifference(arr):
    arr.sort()
    min_diff = float('inf')
    result = []
    for i in range(len(arr)-1):
        diff = arr[i+1] - arr[i]
        if diff < min_diff:
            min_diff = diff
            result = [[arr[i], arr[i+1]]]
        elif diff == min_diff:
            result.append([arr[i], arr[i+1]])
    return result

print(minimumAbsoluteDifference([4,2,1,3]))
