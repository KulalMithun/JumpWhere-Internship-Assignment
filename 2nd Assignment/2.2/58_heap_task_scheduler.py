from collections import Counter
def leastInterval(tasks, n):
    count = Counter(tasks)
    max_freq = max(count.values())
    max_count = sum(1 for v in count.values() if v == max_freq)
    return max(len(tasks), (max_freq-1)*(n+1)+max_count)

print(leastInterval(["A","A","A","B","B","B"], 2))
