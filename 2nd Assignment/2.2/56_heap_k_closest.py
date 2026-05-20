import heapq
def kClosest(points, k):
    heap = [(-((x**2+y**2)**0.5), x, y) for x, y in points]
    heapq.heapify(heap)
    return [[x, y] for _, x, y in heapq.nlargest(k, heap)]

print(kClosest([[1,3],[-2,2]], 1))
