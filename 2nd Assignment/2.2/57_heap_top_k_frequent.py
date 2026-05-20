import heapq
from collections import Counter
def topKFrequent(nums, k):
    count = Counter(nums)
    return [num for num, _ in heapq.nlargest(k, count.items(), key=lambda x: x[1])]

print(topKFrequent([1,1,1,2,2,3], 2))
