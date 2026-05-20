def twoSum(nums, target):
    seen = {}
    for i,num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print(twoSum([2,7,11,15], 9))
