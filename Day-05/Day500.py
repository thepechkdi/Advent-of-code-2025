def parse_input(filename="input.txt"):
    with open(filename, "r") as f:
        sections = f.read().strip().split("\n\n")

    range_lines = sections[0].split("\n")
    id_lines = sections[1].split("\n")

    # Parse ranges
    ranges = []
    for line in range_lines:
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    # Parse available IDs
    ids = list(map(int, id_lines))

    return ranges, ids


def is_fresh(id_value, ranges):
    """Check if id_value is inside ANY range."""
    for start, end in ranges:
        if start <= id_value <= end:
            return True
    return False


def solve_part1(filename="input.txt"):
    ranges, available_ids = parse_input(filename)

    fresh_count = sum(1 for id_value in available_ids if is_fresh(id_value, ranges))

    return fresh_count


# Run solution
print(solve_part1("input.txt"))
