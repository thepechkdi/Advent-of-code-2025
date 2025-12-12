class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n  # track how many disjoint sets

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False  # no merge
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True  # merged


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


def build_edges(points):
    """Return list of (dist_sq, i, j) for all pairs."""
    edges = []
    n = len(points)
    for i in range(n):
        x1, y1, z1 = points[i]
        for j in range(i + 1, n):
            x2, y2, z2 = points[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist_sq = dx * dx + dy * dy + dz * dz
            edges.append((dist_sq, i, j))
    edges.sort(key=lambda e: e[0])
    return edges


def solve_day8_part1(filename: str = "input.txt", num_connections: int = 1000) -> int:
    """
    Part 1:
    Connect the num_connections closest pairs, then
    return the product of the sizes of the three largest circuits.
    """
    points = parse_input(filename)
    n = len(points)
    edges = build_edges(points)

    dsu = DSU(n)
    limit = min(num_connections, len(edges))

    for k in range(limit):
        _, i, j = edges[k]
        dsu.union(i, j)

    # Compute final component sizes
    comp_sizes = {}
    for i in range(n):
        root = dsu.find(i)
        comp_sizes[root] = comp_sizes.get(root, 0) + 1

    sizes = sorted(comp_sizes.values(), reverse=True)
    if len(sizes) < 3:
        raise ValueError("Less than 3 circuits; cannot compute product of three largest.")

    return sizes[0] * sizes[1] * sizes[2]


def solve_day8_part2(filename: str = "input.txt") -> int:
    """
    Part 2:
    Keep connecting closest pairs until all boxes are in one circuit.
    Return the product of the X coordinates of the last two boxes connected.
    """
    points = parse_input(filename)
    n = len(points)
    edges = build_edges(points)

    dsu = DSU(n)

    last_i = last_j = None

    for dist_sq, i, j in edges:
        # If this edge connects two different components, merge them
        if dsu.union(i, j):
            last_i, last_j = i, j
            if dsu.components == 1:
                # All boxes are now in a single circuit
                break

    if last_i is None or last_j is None:
        raise ValueError("Never formed a single circuit; check input.")

    x1 = points[last_i][0]
    x2 = points[last_j][0]
    return x1 * x2


if __name__ == "__main__":
    print(solve_day8_part2("input.txt"))
