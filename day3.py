filename = 'data/day3.txt'

def solve_part_a(filename):
    # Read input file
    with open(filename) as f:
        lines = f.read().strip().split('\n')

    total = 0

    for line in lines:
        # Find the largest digit in positions 0 to n-2 (leaving room for ones digit)
        tens_digit = max(line[:-1])
        tens_index = line.index(tens_digit)

        # Find the largest digit after the tens position
        ones_digit = max(line[tens_index + 1:])

        # Form the two-digit number
        two_digit_num = int(tens_digit + ones_digit)
        total += two_digit_num

    return total


def solve_part_b(filename):
    # Read input file
    with open(filename) as f:
        lines = f.read().strip().split('\n')

    total = 0

    for line in lines:
        # Build 12-digit number greedily
        result_digits = []
        remaining = line

        for _ in range(12):
            # Find the largest digit in positions that leave room for remaining digits
            digits_needed = 12 - len(result_digits)
            search_end = len(remaining) - digits_needed + 1

            # Find the largest digit in the valid range
            max_digit = max(remaining[:search_end])
            max_index = remaining.index(max_digit)

            # Add this digit to result and continue with remaining string
            result_digits.append(max_digit)
            remaining = remaining[max_index + 1:]

        # Form the 12-digit number
        twelve_digit_num = int(''.join(result_digits))
        total += twelve_digit_num

    return total


part_a = solve_part_a(filename)
part_b = solve_part_b(filename)

print(f"Part A: {part_a}")
print(f"Part B: {part_b}")
