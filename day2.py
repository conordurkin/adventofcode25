def solve_part_a(filename):
    # Read input file
    with open(filename) as f:
        data = f.read().strip()

    # Parse the IDs
    ids = set()

    # Split by commas to get individual ranges
    ranges = data.split(',')

    for range_str in ranges:
        if '-' in range_str:
            # Split on the last dash to handle negative numbers if needed
            parts = range_str.split('-')
            start = int(parts[0])
            end = int(parts[1])
            # Add all IDs in the range (inclusive)
            for id_num in range(start, end + 1):
                ids.add(id_num)
        else:
            # Single ID
            ids.add(int(range_str))

    # Initialize counter
    counter = 0

    # Process each ID
    for id_num in ids:
        num_str = str(id_num)
        num_digits = len(num_str)

        # Keep only entries with even number of digits
        if num_digits % 2 == 0:
            # Cut the number in half
            mid = num_digits // 2
            left_half = num_str[:mid]
            right_half = num_str[mid:]

            # If halves are identical, add the number to counter
            if left_half == right_half:
                counter += id_num

    return counter


def solve_part_b(filename):
    # Read input file
    with open(filename) as f:
        data = f.read().strip()

    # Parse the IDs (same as Part A)
    ids = set()
    ranges = data.split(',')

    for range_str in ranges:
        if '-' in range_str:
            parts = range_str.split('-')
            start = int(parts[0])
            end = int(parts[1])
            for id_num in range(start, end + 1):
                ids.add(id_num)
        else:
            ids.add(int(range_str))

    # Initialize counter
    counter = 0

    # Process each ID
    for id_num in ids:
        num_str = str(id_num)
        num_len = len(num_str)

        # Try all possible pattern lengths (from 1 to half the total length)
        found_pattern = False
        for pattern_len in range(1, num_len):
            # Check if this pattern length divides evenly into the total length
            if num_len % pattern_len == 0:
                # Extract the pattern
                pattern = num_str[:pattern_len]
                # Check if the entire number is this pattern repeated
                repetitions = num_len // pattern_len
                if pattern * repetitions == num_str:
                    found_pattern = True
                    break

        if found_pattern:
            counter += id_num

    return counter

filename = 'data/day2.txt'

part_a = solve_part_a(filename)
part_b = solve_part_b(filename)

print(f"Part A: {part_a}")
print(f"Part B: {part_b}")
