def is_invalid_id(n: int) -> bool:
    """
    Returns True if the number n is an invalid ID.
    An invalid ID is a number whose digits are composed
    of some sequence repeated twice.
    """

    s = str(n)                 # Convert number to string
    length = len(s)

    # If length is odd → it can't be repeated twice equally
    if length % 2 != 0:
        return False

    half = length // 2
    left = s[:half]           # First half of the digits
    right = s[half:]          # Second half of the digits

    return left == right      # Check if halves match


def solve(input_line: str) -> int:
    """
    Takes the puzzle input (one long line of ranges)
    and returns the sum of all invalid IDs found.
    """

    total_sum = 0

    # Split by commas: example "11-22,95-115,998-1012"
    ranges = input_line.split(",")

    for r in ranges:
        if not r.strip():
            continue

        start, end = r.split("-")
        start = int(start)
        end = int(end)

        # Go through each number in the range
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total_sum += num

    return total_sum


# --- Read input from file ---
with open("input.text", "r") as f:
    input_line = f.read().strip()   # read the whole line

# --- Solve and print the answer ---
result = solve(input_line)
print("Answer:", result)

