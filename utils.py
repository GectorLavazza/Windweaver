def get_neighbour_matrix(m, x, y):
    neighbour_matrix = []

    for dy in range(-1, 2):
        row = []
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(m) and 0 <= nx < len(
                    m[0]):
                if ny == y and nx == x:
                    row.append("N")
                else:
                    row.append(m[ny][nx])
            else:
                row.append('None')
        neighbour_matrix.append(row)

    return neighbour_matrix


def get_neighbours(m, x, y):
    rows, cols = range(len(m)), range(len(m[0]))
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0),
               (1, 1)]
    result = []
    for dy, dx in offsets:
        ny, nx = y - 1 + dy, x - 1 + dx
        if ny in rows and nx in cols:
            result.append(m[ny][nx])

    return result
