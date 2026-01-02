filename = 'data/day9.txt'


def solve_part_a(filename):
    # Read input file
    with open(filename) as f:
        data = f.read().strip()

    # Parse coordinates
    points = []
    for line in data.split('\n'):
        x, y = map(int, line.split(','))
        points.append((x, y))

    # Find the two points that create the largest rectangle
    max_area = 0
    best_pair = None

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]

            # Calculate area of rectangle with these as diagonal corners
            # Add 1 to include both endpoints (from outside edge to outside edge)
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height

            if area > max_area:
                max_area = area
                best_pair = (points[i], points[j])

    return max_area


def solve_part_b(filename):
    # Read input file
    with open(filename) as f:
        data = f.read().strip()

    # Parse coordinates as a path
    path = []
    for line in data.split('\n'):
        x, y = map(int, line.split(','))
        path.append((x, y))

    # Coordinate compression - extract unique x and y values
    xs = sorted(set(x for x, y in path))
    ys = sorted(set(y for x, y in path))

    # Create mapping from original to compressed coordinates
    x_to_compressed = {x: i for i, x in enumerate(xs)}
    y_to_compressed = {y: i for i, y in enumerate(ys)}

    def compress(point):
        return (x_to_compressed[point[0]], y_to_compressed[point[1]])

    # Compress the path
    compressed_path = [compress(p) for p in path]

    # Build the boundary in compressed space
    boundary = set()
    for i in range(len(compressed_path)):
        x1, y1 = compressed_path[i]
        x2, y2 = compressed_path[(i + 1) % len(compressed_path)]

        if x1 == x2:  # Vertical line
            for y in range(min(y1, y2), max(y1, y2) + 1):
                boundary.add((x1, y))
        else:  # Horizontal line
            for x in range(min(x1, x2), max(x1, x2) + 1):
                boundary.add((x, y1))

    # Flood fill from outside to find all exterior points in compressed space
    # Start from a point that's definitely outside the polygon
    min_cx = min(x for x, y in compressed_path)
    max_cx = max(x for x, y in compressed_path)
    min_cy = min(y for x, y in compressed_path)
    max_cy = max(y for x, y in compressed_path)

    # Expand bounds to ensure we have space outside
    min_cx -= 1
    max_cx += 1
    min_cy -= 1
    max_cy += 1

    start_x = min_cx
    start_y = min_cy

    outside = set()
    queue = [(start_x, start_y)]

    while queue:
        point = queue.pop()
        if point in outside or point in boundary:
            continue

        x, y = point
        # Check bounds
        if x < min_cx or x > max_cx or y < min_cy or y > max_cy:
            continue

        outside.add(point)

        # Add 4-connected neighbors (not 8, to avoid diagonal leaks)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (x + dx, y + dy)
            if neighbor not in outside and neighbor not in boundary:
                queue.append(neighbor)

    # Points inside polygon = boundary + (not outside)
    inside_polygon = set()
    for x in range(min_cx, max_cx + 1):
        for y in range(min_cy, max_cy + 1):
            if (x, y) not in outside:
                inside_polygon.add((x, y))

    # Generate all rectangle candidates with original coordinates
    rectangles = []
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            x1, y1 = path[i]
            x2, y2 = path[j]

            if x1 == x2 or y1 == y2:
                continue

            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            rectangles.append((area, path[i], path[j]))

    # Sort by area descending
    rectangles.sort(reverse=True)

    # Check each rectangle in compressed space
    for area, p1, p2 in rectangles:
        c1 = compress(p1)
        c2 = compress(p2)

        min_cx = min(c1[0], c2[0])
        max_cx = max(c1[0], c2[0])
        min_cy = min(c1[1], c2[1])
        max_cy = max(c1[1], c2[1])

        # Check if all compressed points in this rectangle are inside polygon
        all_inside = True
        for cx in range(min_cx, max_cx + 1):
            for cy in range(min_cy, max_cy + 1):
                if (cx, cy) not in inside_polygon:
                    all_inside = False
                    break
            if not all_inside:
                break

        if all_inside:
            return area

    return 0


part_a = solve_part_a(filename)
part_b = solve_part_b(filename)

print(f"Part A: {part_a}")
print(f"Part B: {part_b}")
