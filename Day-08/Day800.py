from math import inf

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        # Union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


def parse_input(filename: str = "input.txt"):
    points = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x_str, y_str, z_str = line.split(",")
            x, y, z = int(x_str), int(y_str), int(z_str)
            points.append((x, y, z))
    return points


def solve_day8(filename: str = "input.txt", num_connections: int = 1000) -> int:
    points = parse_input(filename)
    n = len(points)

    # Build all pairwise distances
    edges = []
    for i in range(n):
        x1, y1, z1 = points[i]
        for j in range(i + 1, n):
            x2, y2, z2 = points[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist_sq = dx * dx + dy * dy + dz * dz
            edges.append((dist_sq, i, j))

    # Sort edges by squared distance
    edges.sort(key=lambda e: e[0])

    dsu = DSU(n)

    # Connect the num_connections closest pairs
    limit = min(num_connections, len(edges))
    for k in range(limit):
        _, i, j = edges[k]
        dsu.union(i, j)

    # Compute component sizes
    comp_sizes = {}
    for i in range(n):
        root = dsu.find(i)
        comp_sizes[root] = comp_sizes.get(root, 0) + 1

    sizes = sorted(comp_sizes.values(), reverse=True)

    if len(sizes) < 3:
        raise ValueError("Less than 3 circuits; cannot compute product of three largest.")

    a, b, c = sizes[0], sizes[1], sizes[2]
    return a * b * c


if __name__ == "__main__":
    print(solve_day8("input.txt", num_connections=1000))
