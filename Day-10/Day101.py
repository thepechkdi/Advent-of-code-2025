# Day10_part2.py
import re
import pulp


def parse_machines(filename: str):
    machines = []
    line_re = re.compile(
        r'\[(?P<lights>[.#]+)\]\s*'
        r'(?P<buttons>(\([^)]*\)\s*)+)'
        r'\{(?P<targets>[^}]*)\}'
    )

    with open(filename, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            m = line_re.match(line)
            if not m:
                raise ValueError(f"Cannot parse line: {line}")

            # buttons: list of lists of indices
            buttons_str = m.group("buttons")
            button_groups = re.findall(r'\(([^)]*)\)', buttons_str)
            buttons = []
            for bg in button_groups:
                bg = bg.strip()
                if bg == "":
                    buttons.append([])  # button that does nothing (should not happen)
                else:
                    buttons.append([int(x) for x in bg.split(",")])

            # targets: joltage vector
            targets = [int(x) for x in m.group("targets").split(",")]

            machines.append((buttons, targets))

    return machines


def min_presses_for_machine(buttons, targets):
    """
    Solve:  A x = b, x >= 0 integer, minimize sum(x)
    where:
      - A[i][j] = 1 if button j affects counter i, else 0
      - b = targets
    """
    n_counters = len(targets)
    n_buttons = len(buttons)

    # Build ILP
    prob = pulp.LpProblem("machine", pulp.LpMinimize)

    x = [pulp.LpVariable(f"x_{j}", lowBound=0, cat="Integer")
         for j in range(n_buttons)]

    # Objective: minimize total presses
    prob += pulp.lpSum(x)

    # Constraints: for each counter i, sum_j A[i][j]*x_j = targets[i]
    for i in range(n_counters):
        prob += pulp.lpSum(
            (1 if i in buttons[j] else 0) * x[j] for j in range(n_buttons)
        ) == targets[i]

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if prob.status != pulp.LpStatusOptimal:
        raise RuntimeError("No optimal integer solution found")

    value = pulp.value(prob.objective)
    return int(round(value))


def solve_part2(filename: str = "input.txt") -> int:
    machines = parse_machines(filename)
    total = 0
    for buttons, targets in machines:
        total += min_presses_for_machine(buttons, targets)
    return total


if __name__ == "__main__":
    print(solve_part2("input.txt"))
