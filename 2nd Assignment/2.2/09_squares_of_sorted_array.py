def sortedSquares(nums):
    n = len(nums)
    result = [0] * n
    for i in range(n):
        result[i] = nums[i] ** 2
    return sorted(result)

print(sortedSquares([-4,-1,0,3,10]))
