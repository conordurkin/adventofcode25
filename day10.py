filename = 'data/day10.txt'


def solve_part_a(filename):
    # Read input file
    with open(filename) as f:
        data = f.read().strip()

    total_presses = 0

    for line in data.split('\n'):
        # Parse the line
        parts = line.split()

        # Extract target diagram (first element, remove brackets)
        target = parts[0][1:-1]  # Remove [ and ]

        # Extract buttons (elements in parentheses)
        buttons = []
        for part in parts[1:]:
            if part.startswith('(') and part.endswith(')'):
                # Parse button indices
                indices_str = part[1:-1]  # Remove ( and )
                if indices_str:  # Not empty
                    indices = [int(x) for x in indices_str.split(',')]
                    buttons.append(indices)
            elif part.startswith('{'):
                # This is joltage requirements, ignore for now
                break

        # Start with all dots
        current = ['.'] * len(target)

        # Find minimum button presses using BFS
        from collections import deque

        queue = deque([(tuple(current), 0)])  # (state, num_presses)
        visited = {tuple(current)}

        while queue:
            state, presses = queue.popleft()

            # Check if we match the target
            if ''.join(state) == target:
                total_presses += presses
                break

            # Try pressing each button
            for button in buttons:
                # Toggle the indices for this button
                new_state = list(state)
                for idx in button:
                    if new_state[idx] == '.':
                        new_state[idx] = '#'
                    else:
                        new_state[idx] = '.'

                new_state_tuple = tuple(new_state)
                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    queue.append((new_state_tuple, presses + 1))

    return total_presses


def solve_part_b(filename):
    # Read input file
    with open(filename) as f:
        data = f.read().strip()

    from scipy.optimize import linprog
    import numpy as np

    total_presses = 0

    for line in data.split('\n'):
        # Parse the line
        parts = line.split()

        # Extract buttons (elements in parentheses)
        buttons = []
        joltage_target = None

        for part in parts[1:]:
            if part.startswith('(') and part.endswith(')'):
                # Parse button indices
                indices_str = part[1:-1]  # Remove ( and )
                if indices_str:  # Not empty
                    indices = tuple(int(x) for x in indices_str.split(','))
                    buttons.append(indices)
            elif part.startswith('{') and part.endswith('}'):
                # Parse joltage requirements
                joltage_str = part[1:-1]  # Remove { and }
                joltage_target = list(int(x) for x in joltage_str.split(','))

        # Build constraint matrix
        # Each row represents a counter, each column represents a button
        n_counters = len(joltage_target)
        n_buttons = len(buttons)

        # A_eq matrix: A_eq @ x = b_eq where x is the number of times each button is pressed
        A_eq = np.zeros((n_counters, n_buttons))
        for button_idx, button in enumerate(buttons):
            for counter_idx in button:
                A_eq[counter_idx][button_idx] += 1

        # Objective: minimize sum of all button presses (all coefficients = 1)
        c = np.ones(n_buttons)

        # Solve using linear programming
        # linprog minimizes c^T x subject to A_eq x = b_eq and x >= 0
        result = linprog(c, A_eq=A_eq, b_eq=joltage_target, method='highs',
                        integrality=np.ones(n_buttons))  # Integer solution

        if result.success:
            total_presses += int(round(result.fun))
        else:
            print(f"Failed to solve: {result.message}")

    return total_presses


part_a = solve_part_a(filename)
part_b = solve_part_b(filename)

print(f"Part A: {part_a}")
print(f"Part B: {part_b}")
