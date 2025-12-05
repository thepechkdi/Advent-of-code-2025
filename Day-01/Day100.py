def solve_from_file(filename: str) -> int:
    with open(filename, "r") as f:
        rotations = f.readlines()
    return solve(rotations)


def solve(rotations: list[str]) -> int:
    position = 50
    count_zero = 0

    for line in rotations:
        line = line.strip()
        if not line:
            continue

        direction = line[0]
        distance = int(line[1:])

        if direction == 'L':
            position = (position - distance) % 100
        elif direction == 'R':
            position = (position + distance) % 100
        else:
            raise ValueError(f"Unknown direction: {direction}")

        if position == 0:
            count_zero += 1

    return count_zero


if __name__ == "__main__":
    answer = solve_from_file("input.txt")
    print("Password:", answer)
