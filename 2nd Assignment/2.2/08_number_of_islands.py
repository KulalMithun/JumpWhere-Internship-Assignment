def numIslands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    visited = set()
    def dfs(r,c):
        if r<0 or r>=rows or c<0 or c>=cols or grid[r][c]=='0' or (r,c) in visited:
            return
        visited.add((r,c))
        dfs(r+1,c)
        dfs(r-1,c)
        dfs(r,c+1)
        dfs(r,c-1)
    islands = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j]=='1' and (i,j) not in visited:
                dfs(i,j)
                islands += 1
    return islands

print(numIslands([["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]))
