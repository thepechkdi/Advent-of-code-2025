def max_joltage_for_bank(bank: str) -> int:
    """
    Given a string of digits ('987654321111111'),
    return the maximum 2-digit number you can form
    by choosing two digits in order (i < j).
    """

    digits = [int(c) for c in bank.strip()]
    n = len(digits)
    best = -1

    # Try all pairs (i, j) with i < j
    for i in range(n):
        for j in range(i + 1, n):
            value = 10 * digits[i] + digits[j]
            if value > best:
                best = value

    return best

def solve_day3(lines: list[str]) -> int:
    """
    lines: list of strings, each one is a bank of batteries.
    Returns the total sum of max joltages.
    """

    total = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        bank_max = max_joltage_for_bank(line)
        total += bank_max

    return total

if __name__ == "__main__":
    with open("input.text", "r") as f:
        lines = f.readlines()

    answer = solve_day3(lines)
    print("Total output joltage:", answer)

