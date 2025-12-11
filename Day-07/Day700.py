def count_splits(filename: str = "input.txt") -> int:
    # Read grid
    with open(filename, "r") as f:
        grid = [line.rstrip("\n") for line in f]

    height = len(grid)
    width = len(grid[0])

    # Find the starting point S
    start_row = start_col = None
    for r, row in enumerate(grid):
        c = row.find("S")
        if c != -1:
            start_row, start_col = r, c
            break

    if start_row is None:
        raise ValueError("No starting point 'S' found in the grid.")

    # Set of columns containing beams in the current row
    beams = {start_col}
    split_count = 0

    # Process from the row of S down to the second-to-last row
    for r in range(start_row, height - 1):
        next_beams = set()

        for c in beams:
            # Ignore out-of-bounds just in case
            if not (0 <= c < width):
                continue

            cell = grid[r + 1][c]

            if cell == ".":
                # Beam goes straight down
                next_beams.add(c)
            elif cell == "^":
                # Beam is split
                split_count += 1
                if c - 1 >= 0:
                    next_beams.add(c - 1)
                if c + 1 < width:
                    next_beams.add(c + 1)
            else:
                # Any unexpected character: treat as empty space
                next_beams.add(c)

        beams = next_beams
        if not beams:
            # All beams have exited or been blocked
            break

    return split_count


if __name__ == "__main__":
    print(count_splits("input.txt"))
