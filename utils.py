def get_neighbour_matrix(array, x, y):
    # Create an empty matrix to store neighbors
    neighbour_matrix = []

    # Iterate over the rows around the given (x, y) position
    for dy in range(-1, 2):  # -1 to 1 (top, current, bottom row)
        row = []
        for dx in range(-1, 2):  # -1 to 1 (left, current, right column)
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(array) and 0 <= nx < len(
                    array[0]):  # Boundary check
                if ny == y and nx == x:
                    row.append("N")  # Replace the target element with "N"
                else:
                    row.append(array[ny][nx])  # Add neighbor element
            else:
                row.append(None)  # Out of bounds
        neighbour_matrix.append(row)

    return neighbour_matrix


# Example usage
array = [[1, 2, 3, 4],
         [4, 5, 6, 7],
         [8, 9, 10, 11],
         [11, 12, 13, 14]]
x, y = 3, 1
result = get_neighbour_matrix(array, x, y)
for row in result:
    print(row)
