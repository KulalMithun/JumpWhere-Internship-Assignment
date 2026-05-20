import heapq

def find_kth_largest(arr, k):
    arr_negated = [-elem for elem in arr]
    heapq.heapify(arr_negated)
    for i in range(k - 1):
        heapq.heappop(arr_negated)
    return -heapq.heappop(arr_negated)
if __name__ == "__main__":
    print(find_kth_largest([3, 2, 1, 5, 6, 4], 2))
