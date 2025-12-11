def simulate_removals(grid: list[str]) -> int:
    """
    Simulate the process of repeatedly removing all accessible rolls '@':
    - A roll is accessible if it has fewer than 4 neighboring '@' in the 8 directions.
    - Once removed, the grid changes and we may remove more rolls.
    Return the total number of rolls removed.
    """

    # Convert to list of lists for easy modification
    g = [list(row) for row in grid]
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1),
    ]

    total_removed = 0

    while True:
        to_remove = []

        # 1) Find all accessible rolls in the current grid
        for r in range(rows):
            for c in range(cols):
                if g[r][c] != '@':
                    continue

                neighbor_count = 0
                for dr, dc in directions:
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if g[nr][nc] == '@':
                            neighbor_count += 1

                if neighbor_count < 4:
                    to_remove.append((r, c))

        # 2) If none found, stop
        if not to_remove:
            break

        # 3) Remove them all at once
        for (r, c) in to_remove:
            g[r][c] = '.'  # roll removed

        # 4) Increase global count
        total_removed += len(to_remove)

    return total_removed
if __name__ == "__main__":
    with open("input.text", "r") as f:   
        lines = [line.rstrip("\n") for line in f if line.strip()]

    result = simulate_removals(lines)
    print("Total rolls removed:", result)