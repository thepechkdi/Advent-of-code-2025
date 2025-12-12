import re
from collections import deque
from typing import List


def parse_machine_line(line: str):
    """
    Parse one machine line of the form:
    [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

    Returns:
      pattern: string like ".##."
      buttons: list of lists of ints, e.g. [[3], [1,3], [2], ...]
    """
    line = line.strip()
    if not line:
        return None, None

    # Extract pattern inside [ ... ]
    start_br = line.index('[')
    end_br = line.index(']')
    pattern = line[start_br + 1:end_br]  # e.g. ".##."

    # Extract all (...) groups (button wiring schematics)
    # The last {...} is ignored automatically by limiting ourselves to parentheses.
    button_groups = re.findall(r'\(([^)]*)\)', line)

    buttons: List[List[int]] = []
    for grp in button_groups:
        grp = grp.strip()
        if grp == "":
            # Empty group (unlikely in this puzzle, but just in case)
            buttons.append([])
        else:
            nums = [int(x) for x in grp.split(',')]
            buttons.append(nums)

    return pattern, buttons


def min_presses_for_machine(pattern: str, buttons: List[List[int]]) -> int:
    """
    Given a pattern string like ".##." and a list of buttons (each a list of indices),
    compute the minimum number of button presses to reach the target configuration
    from the all-off state.
    """
    L = len(pattern)

    # Target mask
    target = 0
    for i, ch in enumerate(pattern):
        if ch == '#':
            target |= (1 << i)   # bit i corresponds to light i

    # Precompute button masks
    mask_list = []
    for grp in buttons:
        mask = 0
        for idx in grp:
            mask |= (1 << idx)
        mask_list.append(mask)

    # BFS over all states 0..(2^L-1)
    nstates = 1 << L
    dist = [-1] * nstates
    dq = deque()

    start = 0
    dist[start] = 0
    dq.append(start)

    while dq:
        s = dq.popleft()
        # If we've reached the target configuration
        if s == target:
            return dist[s]
        # Try pressing each button once
        for m in mask_list:
            ns = s ^ m
            if dist[ns] == -1:
                dist[ns] = dist[s] + 1
                dq.append(ns)

    # If somehow unreachable (shouldn't happen in this puzzle)
    return -1


def solve(filename: str = "input.txt") -> int:
    total_presses = 0
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            pattern, buttons = parse_machine_line(line)
            if pattern is None:
                continue
            presses = min_presses_for_machine(pattern, buttons)
            total_presses += presses
    return total_presses


if __name__ == "__main__":
    answer = solve("input.txt")
    print(answer)
