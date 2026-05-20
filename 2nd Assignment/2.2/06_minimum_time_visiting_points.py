def minimumTime(points):
    time = 0
    x,y = 0,0
    for nx,ny in points:
        time += max(abs(nx-x), abs(ny-y))
        x,y = nx,ny
    return time

print(minimumTime([[1,2],[3,3],[2,2]]))
