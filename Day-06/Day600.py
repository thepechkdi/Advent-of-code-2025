def solve_day6(filename="input.text"):
    # --- Read and normalize lines ---
    with open(filename, "r") as f:
        rows = [line.rstrip("\n") for line in f]

    if not rows:
        return 0

    height = len(rows)
    width = max(len(r) for r in rows)

    # Pad all rows to same width with spaces
    rows = [r.ljust(width) for r in rows]

    # --- Find separator columns (full column of spaces) ---
    is_sep = []
    for c in range(width):
        if all(rows[r][c] == " " for r in range(height)):
            is_sep.append(True)
        else:
            is_sep.append(False)

    # --- Group columns into problem blocks ---
    blocks = []
    start = None
    for c in range(width):
        if not is_sep[c]:        # part of a problem
            if start is None:
                start = c
        else:                    # separator column
            if start is not None:
                blocks.append((start, c - 1))
                start = None
    if start is not None:
        blocks.append((start, width - 1))

    total = 0
    last_row_idx = height - 1

    # --- Process each block (problem) ---
    for start_col, end_col in blocks:
        # 1) Find operator in the last row of this block
        op_segment = rows[last_row_idx][start_col:end_col + 1]
        if "+" in op_segment:
            op = "+"
        elif "*" in op_segment:
            op = "*"
        else:
            # No operator found, skip (should not happen in valid input)
            continue

        # 2) Extract numbers above the operator row
        numbers = []
        for r in range(last_row_idx):
            segment = rows[r][start_col:end_col + 1]
            s = segment.strip()
            if s:   # not empty
                # should be a number
                numbers.append(int(s))

        if not numbers:
            continue

        # 3) Compute value of this problem
        if op == "+":
            value = sum(numbers)
        else:  # op == "*"
            value = 1
            for n in numbers:
                value *= n

        total += value

    return total


if __name__ == "__main__":
    print(solve_day6("input.text"))
