import heapq
def findCheapestPrice(n, flights, src, dst, k):
    graph = [[] for _ in range(n)]
    for u, v, w in flights:
        graph[u].append((v, w))
    pq = [(0, src, 0)]
    visited = {}
    while pq:
        price, node, stops = heapq.heappop(pq)
        if node == dst:
            return price
        if stops > k:
            continue
        if node in visited and visited[node] <= stops:
            continue
        visited[node] = stops
        for neighbor, w in graph[node]:
            heapq.heappush(pq, (price+w, neighbor, stops+1))
    return -1
