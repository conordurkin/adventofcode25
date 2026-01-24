filename = 'data/day12.txt'


def parse_input(filename):
    """Parse shapes and regions from input file"""
    with open(filename) as f:
        lines = f.read().strip().split('\n')

    # Parse shapes (each shape is: "N:" followed by 3 lines of the 3x3 grid)
    shapes = {}
    i = 0
    while i < len(lines) and ':' in lines[i] and 'x' not in lines[i]:
        shape_id = int(lines[i].rstrip(':'))
        grid = [lines[i+1], lines[i+2], lines[i+3]]
        # Store both size and the grid pattern
        size = sum(1 for row in grid for ch in row if ch == '#')
        shapes[shape_id] = {'size': size, 'grid': grid}
        i += 5

    # Parse regions (format: "WxH: n0 n1 n2 n3 n4 n5")
    regions = []
    while i < len(lines):
        if lines[i].strip():
            parts = lines[i].split(': ')
            dims = parts[0].split('x')
            width, height = int(dims[0]), int(dims[1])
            counts = list(map(int, parts[1].split()))
            regions.append((width, height, counts))
        i += 1

    return shapes, regions


def get_orientations(grid):
    """Generate all unique orientations of a shape grid"""
    def rotate_90(g):
        return [''.join(g[len(g)-1-j][i] for j in range(len(g))) for i in range(len(g[0]))]

    def flip_h(g):
        return [row[::-1] for row in g]

    orientations = set()
    current = grid
    for _ in range(2):
        for _ in range(4):
            orientations.add(tuple(current))
            current = rotate_90(current)
        current = flip_h(current)

    return [list(o) for o in orientations]


def solve_with_backtracking(width, height, counts, shapes):
    """MRV backtracking solver for edge cases"""
    # Precompute orientations for each shape
    shape_orientations = {sid: get_orientations(shapes[sid]['grid']) for sid in shapes}
    shape_sizes = {sid: shapes[sid]['size'] for sid in shapes}

    def can_place(grid, shape, x, y):
        if y + len(shape) > height or x + len(shape[0]) > width:
            return None
        positions = []
        for i, row in enumerate(shape):
            for j, ch in enumerate(row):
                if ch == '#':
                    if grid[y + i][x + j] == '#':
                        return None
                    positions.append((y + i, x + j))
        return positions

    def get_placements(grid, shape_id):
        placements = []
        for shape in shape_orientations[shape_id]:
            for y in range(height - len(shape) + 1):
                for x in range(width - len(shape[0]) + 1):
                    pos = can_place(grid, shape, x, y)
                    if pos:
                        placements.append(pos)
        return placements

    def solve(grid, remaining):
        if sum(remaining) == 0:
            return True

        # Early exit: not enough space
        empty = sum(1 for row in grid for ch in row if ch == '.')
        needed = sum(remaining[i] * shape_sizes[i] for i in range(len(remaining)) if remaining[i] > 0)
        if empty < needed:
            return False

        # MRV: pick shape with fewest placements
        best, best_placements = None, None
        for i in range(len(remaining)):
            if remaining[i] > 0:
                placements = get_placements(grid, i)
                if not placements:
                    return False
                if best is None or len(placements) < len(best_placements):
                    best, best_placements = i, placements

        for positions in best_placements:
            for py, px in positions:
                grid[py][px] = '#'
            remaining[best] -= 1

            if solve(grid, remaining):
                return True

            remaining[best] += 1
            for py, px in positions:
                grid[py][px] = '.'

        return False

    grid = [['.' for _ in range(width)] for _ in range(height)]
    return solve(grid, list(counts))


def solve_part_a(filename):
    """Count how many regions can fit all their required shapes"""
    shapes, regions = parse_input(filename)

    solvable = 0
    for width, height, counts in regions:
        grid_area = width * height
        shape_area = sum(counts[sid] * shapes[sid]['size'] for sid in range(len(counts)))
        total_shapes = sum(counts)

        if shape_area > grid_area:
            # Impossible - shapes need more cells than grid has
            pass
        elif total_shapes * 9 <= grid_area:
            # 3x3 shortcut: definitely solvable
            solvable += 1
        else:
            # Edge case: need backtracking
            if solve_with_backtracking(width, height, counts, shapes):
                solvable += 1

    return solvable

part_a = solve_part_a(filename)

print(f"Part A: {part_a}")