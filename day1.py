def solve_part_a(filename):
    # Read input file
    with open(filename) as f:
        lines = f.read().strip().split('\n')

    # Start at 50
    total = 50
    zero_count = 0

    # Process each instruction
    for line in lines:
        direction, value = line[0], int(line[1:])

        # Apply the operation
        if direction == 'L':
            total -= value
        else:  # direction == 'R'
            total += value

        # Apply wrapping rules (may need to apply multiple times)
        while total < 0:
            total += 100
        while total > 99:
            total -= 100

        # Count if we hit exactly zero
        if total == 0:
            zero_count += 1

    return total, zero_count

def solve_part_b(filename):
    # Read input file
    with open(filename) as f:
        lines = f.read().strip().split('\n')

    # Start at 50
    total = 50
    zero_passes = 0

    # Process each instruction
    for line in lines:
        direction, value = line[0], int(line[1:])
        prev_total = total
        new_total = total - value if direction == 'L' else total + value

        # Determine range of movement
        min_val, max_val = (new_total, prev_total) if direction == 'L' else (prev_total, new_total)

        # Find first multiple of 100 to check
        start_multiple = 0 if min_val >= 0 else ((min_val // 100) - 1) * 100

        # Count all multiples of 100 crossed (excluding starting position)
        current = start_multiple
        while current <= max_val:
            if current % 100 == 0 and current > min_val and current <= max_val and current != prev_total:
                zero_passes += 1
            elif current == new_total and new_total % 100 == 0 and current >= min_val and current != prev_total:
                zero_passes += 1
            current += 100

        # Apply wrapping
        total = new_total % 100

    return total, zero_passes


filename = 'data/day1.txt'

_, part_a = solve_part_a(filename)
_, part_b = solve_part_b(filename)

print(f"Part A: {part_a}")
print(f"Part B: {part_b}")
