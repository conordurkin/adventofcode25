filename = 'data/day11.txt'


def solve_part_a(filename):
    # Read input file
    with open(filename) as f:
        data = f.read().strip()

    # Parse the graph
    graph = {}
    for line in data.split('\n'):
        parts = line.split(': ')
        node = parts[0]
        neighbors = parts[1].split()
        graph[node] = neighbors

    # DFS to count all paths from "you" to "out"
    def count_paths(current, target, visited):
        # Base case: reached the target
        if current == target:
            return 1

        # Mark current node as visited (for this path)
        visited.add(current)

        # Count paths through all neighbors
        total_paths = 0
        for neighbor in graph.get(current, []):
            if neighbor not in visited:  # Avoid cycles
                total_paths += count_paths(neighbor, target, visited)

        # Backtrack: unmark current node so other paths can use it
        visited.remove(current)

        return total_paths

    # Start from "you" and count paths to "out"
    result = count_paths("you", "out", set())
    return result


def solve_part_b(filename):
    # Read input file
    with open(filename) as f:
        data = f.read().strip()

    # Parse the graph
    graph = {}
    for line in data.split('\n'):
        parts = line.split(': ')
        node = parts[0]
        neighbors = parts[1].split()
        graph[node] = neighbors

    # Dynamic Programming approach
    # Key insight: The graph is a DAG (no cycles), so we can use DP
    # State: (current_node, seen_fft, seen_dac)
    # We don't need to track visited set because there are no cycles

    from functools import lru_cache

    # Make graph immutable for hashing
    graph_tuple = {k: tuple(v) for k, v in graph.items()}

    @lru_cache(maxsize=None)
    def count_paths(current, seen_fft, seen_dac):
        """Count paths from current to 'out' that visit both fft and dac"""
        # Base case: reached destination
        if current == "out":
            return 1 if (seen_fft and seen_dac) else 0

        # Update state based on current node
        new_seen_fft = seen_fft or (current == 'fft')
        new_seen_dac = seen_dac or (current == 'dac')

        # Sum paths through all neighbors
        total = 0
        for neighbor in graph_tuple.get(current, ()):
            total += count_paths(neighbor, new_seen_fft, new_seen_dac)

        return total

    result = count_paths('svr', False, False)
    return result


part_a = solve_part_a(filename)
part_b = solve_part_b(filename)

print(f"Part A: {part_a}")
print(f"Part B: {part_b}")
