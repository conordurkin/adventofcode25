filename = 'data/day5.txt'


def solve_part_a(filename):
    # Read input file
    with open(filename) as f:
        data = f.read().strip()

    # Split on blank line
    sections = data.split('\n\n')
    ranges_section = sections[0]
    numbers_section = sections[1]

    # Parse ranges into list of (start, end) tuples
    ranges = []
    for line in ranges_section.split('\n'):
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

    # Parse individual numbers into a list
    individual_numbers = [int(line) for line in numbers_section.split('\n')]

    # Count how many individual numbers fall within any range
    count = 0
    for num in individual_numbers:
        for start, end in ranges:
            if start <= num <= end:
                count += 1
                break  # Found a match, no need to check other ranges

    return count


def solve_part_b(filename):
    # Read input file
    with open(filename) as f:
        data = f.read().strip()

    # Split on blank line
    sections = data.split('\n\n')
    ranges_section = sections[0]

    # Parse ranges and merge overlapping ones
    ranges = []
    for line in ranges_section.split('\n'):
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

    # Sort ranges by start position
    ranges.sort()

    # Merge overlapping ranges
    merged = []
    for start, end in ranges:
        if merged and start <= merged[-1][1] + 1:
            # Overlaps or adjacent with the last merged range
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            # No overlap, add as new range
            merged.append((start, end))

    # Count unique integers across all merged ranges
    total_count = 0
    for start, end in merged:
        total_count += (end - start + 1)

    return total_count


part_a = solve_part_a(filename)
part_b = solve_part_b(filename)

print(f"Part A: {part_a}")
print(f"Part B: {part_b}")
