def solve_day6_part2(filename="input.text"):
    # --- Read and normalize lines ---
    with open(filename, "r") as f:
        rows = [line.rstrip("\n") for line in f]

    if not rows:
        return 0

    height = len(rows)
    width = max(len(r) for r in rows)
    rows = [r.ljust(width) for r in rows]

    # --- Identify separator columns (all spaces) ---
    is_sep = []
    for c in range(width):
        if all(rows[r][c] == " " for r in range(height)):
            is_sep.append(True)
        else:
            is_sep.append(False)

    # --- Group contiguous non-separator columns into blocks (problems) ---
    blocks = []
    start = None
    for c in range(width):
        if not is_sep[c]:          # part of a problem
            if start is None:
                start = c
        else:                      # separator column
            if start is not None:
                blocks.append((start, c - 1))
                start = None
    if start is not None:
        blocks.append((start, width - 1))

    total = 0

    # --- Process each problem block ---
    for start_col, end_col in blocks:
        # 1) Find operator row (bottom-most row in which this block has + or *)
        op = None
        op_row = None
        for r in range(height - 1, -1, -1):
            segment = rows[r][start_col:end_col + 1]
            if "+" in segment:
                op = "+"
                op_row = r
                break
            if "*" in segment:
                op = "*"
                op_row = r
                break

        if op is None or op_row is None:
            continue  # malformed block; should not happen in valid input

        # 2) Read numbers column by column, RIGHT to LEFT
        numbers = []
        for c in range(end_col, start_col - 1, -1):
            digits = []
            for r in range(op_row):      # above operator row only
                ch = rows[r][c]
                if ch.isdigit():
                    digits.append(ch)
            if digits:
                num = int("".join(digits))
                numbers.append(num)

        if not numbers:
            continue

        # 3) Compute this problem's result
        if op == "+":
            value = sum(numbers)
        else:  # op == "*"
            value = 1
            for n in numbers:
                value *= n

        total += value

    return total


if __name__ == "__main__":
    print(solve_day6_part2("input.text"))
