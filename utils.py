def get_neighbours(m,x,y):
    rows, cols = range(len(m)),range(len(m[0]))
    offsets = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    result = []
    for dy,dx in offsets:
        ny, nx = y+dy, x+dx
        if ny in rows and nx in cols:
            result.append(m[ny][nx])
    return result
