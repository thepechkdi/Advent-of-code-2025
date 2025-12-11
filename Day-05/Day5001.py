def solve_part2(filename="input.txt"):
    ranges = []

    # --- Read only the ranges (stop at first blank line) ---
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:  # stop when blank line appears
                break
            start, end = map(int, line.split("-"))
            if start > end:
                start, end = end, start
            ranges.append((start, end))

    if not ranges:
        return 0

    # --- Merge overlapping ranges ---
    ranges.sort()
    merged = []
    cur_start, cur_end = ranges[0]

    for start, end in ranges[1:]:
        if start <= cur_end + 1:  # overlapping or touching
            cur_end = max(cur_end, end)
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = start, end

    merged.append((cur_start, cur_end))

    # --- Count total IDs covered ---
    total_fresh = sum((end - start + 1) for start, end in merged)
    return total_fresh


if __name__ == "__main__":
    print(solve_part2("input.txt"))
