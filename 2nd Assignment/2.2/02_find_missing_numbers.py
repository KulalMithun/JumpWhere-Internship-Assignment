def findDisappearedNumbers(nums):
    n = len(nums)
    return list(set(range(1,n+1)) - set(nums))

print(findDisappearedNumbers([4,3,2,7,8,2,3,1]))
