def minSubArrayLen(target, nums):
    left = 0
    total = 0
    min_len = float('inf')
    for right in range(len(nums)):
        total += nums[right]
        while total >= target:
            min_len = min(min_len, right-left+1)
            total -= nums[left]
            left += 1
    return min_len if min_len != float('inf') else 0

print(minSubArrayLen(7, [2,3,1,2,4,3]))
