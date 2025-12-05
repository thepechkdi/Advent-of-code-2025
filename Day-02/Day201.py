def is_invalid_id_part2(n: int) -> bool:
    """
    Part 2 rule:
    An ID is invalid if it consists of some sequence of digits
    repeated at least twice (2, 3, 4... times).
    Example: 123123, 123123123, 11, 111111
    """

    s = str(n)
    L = len(s)

    # Try all possible block lengths
    # from 1 up to half of the length
    for block_len in range(1, L // 2 + 1):
        # The total length must be a multiple of block_len
        if L % block_len != 0:
            continue

        block = s[:block_len]
        repeats = L // block_len

        # block repeated "repeats" times must equal the full string
        if block * repeats == s and repeats >= 2:
            return True

    return False
def solve_part2(input_line: str) -> int:
    total_sum = 0

    # Split by commas: "11-22,95-115,998-1012,..."
    ranges = input_line.split(",")

    for r in ranges:
        r = r.strip()
        if not r:
            continue

        start_str, end_str = r.split("-")
        start = int(start_str)
        end = int(end_str)

        for num in range(start, end + 1):
            if is_invalid_id_part2(num):
                total_sum += num

    return total_sum
if __name__ == "__main__":
    with open("input.text", "r") as f:
        input_line = f.read().strip()

    answer_part2 = solve_part2(input_line)
    print("Part 2 answer:", answer_part2)
