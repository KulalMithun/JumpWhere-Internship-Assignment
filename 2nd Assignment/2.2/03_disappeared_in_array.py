def findDisappearedNumbers(nums):
    n = len(nums)
    seen = set(nums)
    return [i for i in range(1,n+1) if i not in seen]

print(findDisappearedNumbers([4,3,2,7,8,2,3,1]))
