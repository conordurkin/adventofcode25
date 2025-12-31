filename = 'data/day6.txt'


def solve_part_a(filename):
    # Read input file
    with open(filename) as f:
        lines = f.read().strip().split('\n')

    # Parse the data - last row is operators, rest are numbers
    number_rows = lines[:-1]
    operator_row = lines[-1]

    # Split each row by whitespace
    numbers = [line.split() for line in number_rows]
    operators = operator_row.split()

    # Process each column
    total = 0
    num_cols = len(operators)

    for col_idx in range(num_cols):
        # Get all numbers in this column
        column_values = [int(numbers[row_idx][col_idx]) for row_idx in range(len(numbers))]
        operator = operators[col_idx]

        # Apply the operator to combine all values in the column
        if operator == '*':
            result = 1
            for val in column_values:
                result *= val
        elif operator == '+':
            result = sum(column_values)

        total += result

    return total


def solve_part_b(filename):
    # Read input file - preserve exact spacing
    with open(filename) as f:
        lines = f.read().split('\n')

    # Remove empty lines
    lines = [line for line in lines if line]

    # Parse the data - last row is operators, rest are numbers
    number_rows = lines[:-1]
    operator_row = lines[-1]

    # Collect all vertical numbers at each character position
    # Group them by which operator they belong to
    operator_groups = {}  # Maps operator position to list of vertical numbers

    for col_idx in range(len(operator_row)):
        # Read digits vertically at this column position
        vertical_digits = []
        for row in number_rows:
            if col_idx < len(row) and row[col_idx] != ' ':
                vertical_digits.append(row[col_idx])

        # If we found digits, create a number from them
        if vertical_digits:
            number = int(''.join(vertical_digits))

            # Find which operator this column belongs to
            # We need to find the closest non-space character at or before this position
            op_idx = col_idx
            while op_idx >= 0 and operator_row[op_idx] == ' ':
                op_idx -= 1

            if op_idx >= 0:
                if op_idx not in operator_groups:
                    operator_groups[op_idx] = {
                        'operator': operator_row[op_idx],
                        'numbers': []
                    }
                operator_groups[op_idx]['numbers'].append(number)

    # Now apply each operator to its group of numbers
    total = 0
    for op_idx in sorted(operator_groups.keys()):
        group = operator_groups[op_idx]
        operator = group['operator']
        numbers = group['numbers']

        if operator == '*':
            result = 1
            for num in numbers:
                result *= num
        elif operator == '+':
            result = sum(numbers)

        total += result

    return total


part_a = solve_part_a(filename)
part_b = solve_part_b(filename)

print(f"Part A: {part_a}")
print(f"Part B: {part_b}")
