def singleNumber(nums):
    result = 0
    for num in nums:
        result ^= num
    return result

print(singleNumber([2,2,1]))
