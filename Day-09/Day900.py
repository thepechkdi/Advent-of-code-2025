def parse_input(filename="input.txt"):
    points = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x_str, y_str = line.split(",")
            x, y = int(x_str), int(y_str)
            points.append((x, y))
    return points


def largest_rectangle_area(filename="input.txt") -> int:
    points = parse_input(filename)
    n = len(points)
    max_area = 0

    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height
            if area > max_area:
                max_area = area

    return max_area


if __name__ == "__main__":
    print(largest_rectangle_area("input.txt"))
