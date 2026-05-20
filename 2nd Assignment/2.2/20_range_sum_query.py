class NumArray:
    def __init__(self, nums):
        self.prefix = [0] * (len(nums)+1)
        for i in range(len(nums)):
            self.prefix[i+1] = self.prefix[i] + nums[i]
    def sumRange(self, left, right):
        return self.prefix[right+1] - self.prefix[left]

obj = NumArray([-2,0,3,-5,2,-1])
print(obj.sumRange(0, 2))
