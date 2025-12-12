# Day 9 – Part 2 : largest rectangle made only of red + green tiles
# Opposite corners must be red tiles (i.e. among the input points).

from typing import List, Tuple


# ------------------------------------------------------------
# Parsing
# ------------------------------------------------------------
def parse_red_points(filename: str = "input.txt") -> List[Tuple[int, int]]:
    pts: List[Tuple[int, int]] = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y = map(int, line.split(","))
            pts.append((x, y))
    return pts


# ------------------------------------------------------------
# Geometry helpers
# ------------------------------------------------------------
def point_in_or_on_polygon(x: float, y: float,
                           vertices: List[Tuple[int, int]]) -> bool:
    """
    Standard ray-casting test.
    Returns True if (x,y) is inside the polygon or on its boundary.
    """
    inside = False
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]

        # Check if point lies exactly on this edge
        if (min(x1, x2) <= x <= max(x1, x2) and
            min(y1, y2) <= y <= max(y1, y2) and
            (x2 - x1) * (y - y1) == (y2 - y1) * (x - x1)):
            return True

        # Ray to +inf in x direction: does edge cross it?
        if (y1 > y) != (y2 > y):
            x_int = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
            if x_int >= x:
                inside = not inside

    return inside


# ------------------------------------------------------------
# Main solver for Part Two
# ------------------------------------------------------------
def largest_red_green_rectangle(filename: str = "input.txt") -> int:
    red_pts = parse_red_points(filename)

    # Unique sorted X and Y coordinates
    xs = sorted({x for x, _ in red_pts})
    ys = sorted({y for _, y in red_pts})
    nx, ny = len(xs), len(ys)

    # Map coordinate -> index
    x_to_idx = {x: i for i, x in enumerate(xs)}
    y_to_idx = {y: i for i, y in enumerate(ys)}

    # Step 1: build a compressed grid of "cells" between consecutive x,y lines.
    # For each cell, check whether its center lies inside the polygon (red+green region).
    inside = [[False] * (ny - 1) for _ in range(nx - 1)]
    for i in range(nx - 1):
        xm = (xs[i] + xs[i + 1]) / 2.0
        for j in range(ny - 1):
            ym = (ys[j] + ys[j + 1]) / 2.0
            inside[i][j] = point_in_or_on_polygon(xm, ym, red_pts)

    # Step 2: build 2D prefix sum over "inside" cells
    ps = [[0] * ny for _ in range(nx)]
    for i in range(nx - 1):
        row_sum = 0
        for j in range(ny - 1):
            if inside[i][j]:
                row_sum += 1
            ps[i + 1][j + 1] = ps[i][j + 1] + row_sum

    def all_cells_inside(ix1: int, ix2: int, iy1: int, iy2: int) -> bool:
        """
        Check whether all compressed cells in rectangle
        [ix1, ix2) x [iy1, iy2) are marked as inside.
        """
        if ix1 >= ix2 or iy1 >= iy2:
            return False
        total = (ix2 - ix1) * (iy2 - iy1)
        s = ps[ix2][iy2] - ps[ix1][iy2] - ps[ix2][iy1] + ps[ix1][iy1]
        return s == total

    # Step 3: try all pairs of red points as opposite corners of the rectangle
    max_area = 0
    n = len(red_pts)
    for a in range(n):
        x1, y1 = red_pts[a]
        ix1 = x_to_idx[x1]
        iy1 = y_to_idx[y1]
        for b in range(a + 1, n):
            x2, y2 = red_pts[b]

            # Must really be opposite corners (not same row/column)
            if x1 == x2 or y1 == y2:
                continue

            ix2 = x_to_idx[x2]
            iy2 = y_to_idx[y2]

            if ix1 < ix2:
                lx, rx = ix1, ix2
            else:
                lx, rx = ix2, ix1

            if iy1 < iy2:
                ly, ry = iy1, iy2
            else:
                ly, ry = iy2, iy1

            # Check that the whole rectangle between them is red/green only
            if not all_cells_inside(lx, rx, ly, ry):
                continue

            # Area in tile units: inclusive rectangle
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if area > max_area:
                max_area = area

    return max_area


if __name__ == "__main__":
    print(largest_red_green_rectangle("input.txt"))
