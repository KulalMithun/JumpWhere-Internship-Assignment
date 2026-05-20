def containsDuplicate(nums):
    return len(nums) != len(set(nums))

print(containsDuplicate([1,1,1,2,2,54,5,3,6]))
