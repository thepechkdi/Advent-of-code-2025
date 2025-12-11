def count_accessible_rolls(grid: list[str]) -> int:
    """
    grid: list of strings representing the map ('.' and '@').

    Returns the number of rolls '@' that have
    fewer than 4 neighboring '@' in the 8 directions.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # 8 directions: up, down, left, right, and diagonals
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1),
    ]

    accessible = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '@':
                continue

            neighbor_count = 0

            # Check all 8 neighbors
            for dr, dc in directions:
                nr = r + dr
                nc = c + dc

                # Keep inside bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == '@':
                        neighbor_count += 1

            # Forklift can access if fewer than 4 neighbors
            if neighbor_count < 4:
                accessible += 1

    return accessible
if __name__ == "__main__":
    with open("input.text", "r") as f:   
        lines = [line.rstrip("\n") for line in f if line.strip()]

    result = count_accessible_rolls(lines)
    print("Accessible rolls:", result)
