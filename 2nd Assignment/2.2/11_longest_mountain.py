def longestMountain(arr):
    if len(arr) < 3:
        return 0
    longest = 0
    i = 1
    while i < len(arr)-1:
        if arr[i-1] < arr[i] > arr[i+1]:
            left, right = i-1, i+1
            while left > 0 and arr[left-1] < arr[left]:
                left -= 1
            while right < len(arr)-1 and arr[right] > arr[right+1]:
                right += 1
            longest = max(longest, right-left+1)
            i = right+1
        else:
            i += 1
    return longest

print(longestMountain([2,1,4,7,3,2,5]))
