filename = 'data/day8.txt'


def solve_part_a(filename):
    # Read input file
    with open(filename) as f:
        data = f.read().strip()

    # Parse coordinates
    points = []
    for line in data.split('\n'):
        x, y, z = map(int, line.split(','))
        points.append((x, y, z))

    # Calculate distances between all pairs
    import math
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1, z1 = points[i]
            x2, y2, z2 = points[j]
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Use Union-Find to properly handle group merging
    parent = list(range(len(points)))  # Each point starts as its own parent

    def find(x):
        # Find root parent with path compression
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        # Union two sets
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_y] = root_x

    # Process the 1000 closest pairs
    for k in range(1000):
        dist, i, j = distances[k]
        union(i, j)

    # Group points by their root parent
    groups = {}
    for i in range(len(points)):
        root = find(i)
        if root not in groups:
            groups[root] = []
        groups[root].append(i)

    # Filter out singleton groups (only count groups with 2+ points)
    multi_point_groups = {gid: members for gid, members in groups.items() if len(members) > 1}

    # Get group sizes and sort by size (biggest to smallest)
    group_sizes = [len(members) for members in multi_point_groups.values()]
    group_sizes.sort(reverse=True)

    # Multiply the three largest group counts together
    answer = group_sizes[0] * group_sizes[1] * group_sizes[2]

    return answer


def solve_part_b(filename):
    # Read input file
    with open(filename) as f:
        data = f.read().strip()

    # Parse coordinates
    points = []
    for line in data.split('\n'):
        x, y, z = map(int, line.split(','))
        points.append((x, y, z))

    # Calculate distances between all pairs
    import math
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1, z1 = points[i]
            x2, y2, z2 = points[j]
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Use Union-Find to properly handle group merging
    parent = list(range(len(points)))  # Each point starts as its own parent

    def find(x):
        # Find root parent with path compression
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        # Union two sets
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_y] = root_x
            return True  # Merged two different groups
        return False  # Already in same group

    def count_groups():
        # Count unique root parents
        roots = set()
        for i in range(len(points)):
            roots.add(find(i))
        return len(roots)

    # Keep connecting points until we have only one group
    last_i, last_j = None, None
    for dist, i, j in distances:
        if union(i, j):
            last_i, last_j = i, j
            if count_groups() == 1:
                break

    # Return the product of the two x-coordinates
    x1, y1, z1 = points[last_i]
    x2, y2, z2 = points[last_j]
    return x1 * x2


part_a = solve_part_a(filename)
part_b = solve_part_b(filename)

print(f"Part A: {part_a}")
print(f"Part B: {part_b}")
