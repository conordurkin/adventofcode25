filename = 'data/day7.txt'


def solve_part_a(filename):
    # Read input file
    with open(filename) as f:
        lines = f.read().strip().split('\n')

    # Build the grid as a list of lists for easy modification
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0])

    # Find the 'S' in the first line
    start_col = None
    for col_idx in range(cols):
        if grid[0][col_idx] == 'S':
            start_col = col_idx
            break

    # Start the propagation from the S position
    if start_col is not None:
        # Replace the period in the next row with '|'
        if grid[1][start_col] == '.':
            grid[1][start_col] = '|'

    # Process each row starting from row 1
    for row_idx in range(1, rows - 1):  # -1 because we check the next row
        for col_idx in range(cols):
            if grid[row_idx][col_idx] == '|':
                # Try to place '|' in the same column in the next row
                next_row_idx = row_idx + 1

                if grid[next_row_idx][col_idx] == '.':
                    # Direct placement
                    grid[next_row_idx][col_idx] = '|'
                elif grid[next_row_idx][col_idx] == '^':
                    # Check cells before and after the caret
                    if col_idx > 0 and grid[next_row_idx][col_idx - 1] == '.':
                        grid[next_row_idx][col_idx - 1] = '|'
                    if col_idx < cols - 1 and grid[next_row_idx][col_idx + 1] == '.':
                        grid[next_row_idx][col_idx + 1] = '|'

    # Count how many '^' symbols have a '|' directly above them
    count = 0
    for row_idx in range(1, rows):  # Start from row 1 since we check above
        for col_idx in range(cols):
            if grid[row_idx][col_idx] == '^':
                # Check if there's a '|' directly above
                if grid[row_idx - 1][col_idx] == '|':
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

    # Find the 'S' starting position
    start_col = None
    for col_idx in range(cols):
        if grid[0][col_idx] == 'S':
            start_col = col_idx
            break

    # Use DP to count paths
    # paths[row][col] = number of distinct paths to reach (row, col)
    paths = {}
    paths[(0, start_col)] = 1

    # Process row by row
    for row_idx in range(rows - 1):
        # For each position in the current row with paths
        for col_idx in range(cols):
            if (row_idx, col_idx) not in paths:
                continue

            num_paths = paths[(row_idx, col_idx)]
            next_row = row_idx + 1

            # Check what's in the next row at this column
            if grid[next_row][col_idx] == '.':
                # Can go straight down
                if (next_row, col_idx) not in paths:
                    paths[(next_row, col_idx)] = 0
                paths[(next_row, col_idx)] += num_paths
            elif grid[next_row][col_idx] == '^':
                # At a caret, can go left or right
                # Go left
                if col_idx > 0 and grid[next_row][col_idx - 1] == '.':
                    if (next_row, col_idx - 1) not in paths:
                        paths[(next_row, col_idx - 1)] = 0
                    paths[(next_row, col_idx - 1)] += num_paths
                # Go right
                if col_idx < cols - 1 and grid[next_row][col_idx + 1] == '.':
                    if (next_row, col_idx + 1) not in paths:
                        paths[(next_row, col_idx + 1)] = 0
                    paths[(next_row, col_idx + 1)] += num_paths

    # Sum all paths that reach the last row
    total_paths = 0
    for col_idx in range(cols):
        if (rows - 1, col_idx) in paths:
            total_paths += paths[(rows - 1, col_idx)]

    return total_paths


part_a = solve_part_a(filename)
part_b = solve_part_b(filename)

print(f"Part A: {part_a}")
print(f"Part B: {part_b}")
