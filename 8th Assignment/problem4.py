class TwoSum:
    def find_pair(self,numbers,target):
        seen={}
        for i,num in enumerate(numbers):
            diff=target-num
            if diff in seen:
                return seen[diff],i
            seen[num]=i
