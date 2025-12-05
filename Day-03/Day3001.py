def max_joltage_for_bank_12(bank: str, k: int = 12) -> int:
    """
    Given a string of digits ('987654321111111'),
    return the maximum k-digit number you can form
    by choosing k digits in order (subsequence).
    """

    s = bank.strip()
    n = len(s)
    to_drop = n - k   # how many digits we are allowed to remove
    stack = []

    for c in s:
        # While we can still drop digits and the last digit in the
        # stack is smaller than the current one, drop it
        while to_drop > 0 and stack and stack[-1] < c:
            stack.pop()
            to_drop -= 1
        stack.append(c)

    # If still longer than k, truncate to first k digits
    if len(stack) > k:
        stack = stack[:k]

    # Convert the resulting digit string to integer
    return int("".join(stack))

def solve_day3_part2(lines: list[str]) -> int:
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        best_for_bank = max_joltage_for_bank_12(line, k=12)
        total += best_for_bank
    return total

if __name__ == "__main__":
    with open("input.text", "r") as f:   # or "input.txt" if that's your filename
        lines = f.readlines()

    answer = solve_day3_part2(lines)
    print("Part 2 total output joltage:", answer)

