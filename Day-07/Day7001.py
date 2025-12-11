from collections import defaultdict

def count_timelines_quantum(filename: str = "input.txt") -> int:
    # Read the manifold diagram
    with open(filename, "r") as f:
        rows = [line.rstrip("\n") for line in f]

    height = len(rows)
    width = len(rows[0])

    # Find S (start position)
    start_row = start_col = None
    for r, row in enumerate(rows):
        c = row.find("S")
        if c != -1:
            start_row, start_col = r, c
            break

    if start_row is None:
        raise ValueError("No 'S' found in the input grid.")

    # beams[col] = number of timelines with a beam at (current_row, col)
    beams = {start_col: 1}

    # Process from the row of S down through and just below the grid
    # We go to height (inclusive) with a virtual row of '.' below the grid
    for r in range(start_row, height):
        next_beams = defaultdict(int)

        for col, count in beams.items():
            if not (0 <= col < width):
                continue

            # Cell below current row; outside grid is treated as empty '.'
            if r + 1 < height:
                cell = rows[r + 1][col]
            else:
                cell = "."

            if cell == ".":
                # Beam continues straight down
                next_beams[col] += count
            elif cell == "^":
                # Beam splits: left and right, both with 'count' timelines
                if col - 1 >= 0:
                    next_beams[col - 1] += count
                if col + 1 < width:
                    next_beams[col + 1] += count
            else:
                # Any unexpected character, treat as empty
                next_beams[col] += count

        beams = next_beams

        if not beams:
            # All timelines have exited (rare, but safe)
            break

    # Total number of timelines after all journeys
    return sum(beams.values())


if __name__ == "__main__":
    print(count_timelines_quantum("input.txt"))
