filename = 'data/day4.txt'


def solve_part_a(filename):
    # Read input file
    with open(filename) as f:
        lines = f.read().strip().split('\n')

    # Build the grid
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0])

    # Count @ positions with fewer than 4 neighboring @ symbols
    count = 0

    # 8 directions: up, down, left, right, and 4 diagonals
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                # Count neighboring @ symbols
                neighbors = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                        neighbors += 1

                # Check if fewer than 4 neighbors
                if neighbors < 4:
                    count += 1

    return count


def solve_part_b(filename):
    # Read input file
    with open(filename) as f:
        lines = f.read().strip().split('\n')

    # Build the grid
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0])

    # 8 directions: up, down, left, right, and 4 diagonals
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    total_count = 0

    # Keep iterating until no more @ symbols can be removed
    while True:
        # Find all @ positions with fewer than 4 neighbors
        to_remove = []

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    # Count neighboring @ symbols
                    neighbors = 0
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                            neighbors += 1

                    # Check if fewer than 4 neighbors
                    if neighbors < 4:
                        to_remove.append((r, c))

        # If nothing to remove, we're done
        if not to_remove:
            break

        # Add to count and replace with periods
        total_count += len(to_remove)
        for r, c in to_remove:
            grid[r][c] = '.'

    return total_count


part_a = solve_part_a(filename)
part_b = solve_part_b(filename)

print(f"Part A: {part_a}")
print(f"Part B: {part_b}")
