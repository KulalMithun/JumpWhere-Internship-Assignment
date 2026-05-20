def smallerNumbersThanCurrent(nums):
    sorted_nums = sorted(nums)
    return [sorted_nums.index(num) for num in nums]

print(smallerNumbersThanCurrent([8,1,2,2,3]))
