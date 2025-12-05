def solve_part2(rotations: list[str]) -> int:
    position = 50     
    count_zero = 0   

    for line in rotations:
        line = line.strip()
        if not line:
            continue   

        direction = line[0]       
        distance = int(line[1:]) 

    
        if direction == 'L':
            step = -1
        elif direction == 'R':
            step = 1
        else:
            raise ValueError(f" {direction}")

        for _ in range(distance):
        
            position = (position + step) % 100

            if position == 0:
                count_zero += 1

    return count_zero
def read_input(filename: str) -> list[str]:
    with open(filename, "r") as f:
        return f.readlines()

def solve_part2_file(filename: str) -> int:
    rotations = read_input(filename)
    return solve_part2(rotations)

if __name__ == "__main__":
    answer = solve_part2_file("input.txt")
    print("Password (method 0x434C49434B):", answer)
