from prefect import flow, get_run_logger, task

@task
def read_input():
    list1 = []
    with open("input.txt", "r") as file:
        for line in file:
            list2 = list(line.strip())
            list1.append(list2)
    return list1

@flow
def day4_star1():
    logger = get_run_logger()
    grid = read_input()
    # grid = [
    #     list("MMMSXXMASM"),
    #     list("MSAMXMSMSA"),
    #     list("AMXSXMAAMM"),
    #     list("MSAMASMSMX"),
    #     list("XMASAMXAMM"),
    #     list("XXAMMXXAMA"),
    #     list("SMSMSASXSS"),
    #     list("SAXAMASAAA"),
    #     list("MAMMMXMMMM"),
    #     list("MXMXAXMASX")
    # ]
    num_xmas = 0

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    target = "MAS"
    target_backwards = "SAM"

    logger.info(f"rows: {rows}")
    logger.info(f"Cols: {cols}")
    
    # Check diagonally (top-left to bottom-right)
    for r in range(rows - len(target) + 1):
        for c in range(cols - len(target) + 1):
            if c + len(target) <= cols and r + len(target) <= rows:
                word = ''.join(grid[r + i][c + i] for i in range(len(target)))
                if word == target or word == target_backwards:
                    word2=''.join(grid[r + i][c - i + 2] for i in range(len(target)))
                    if word2 == target or word2 == target_backwards:
                        num_xmas += 1
    
    # Check diagonally (top-right to bottom-left)
    # for r in range(rows - len(target) + 1):
    #     for c in range(len(target) - 1, cols):
    #         word = ''.join(grid[r + i][c - i] for i in range(len(target)))
    #         if word == target:
    #             word2=''.join(grid[r+i-2][c+i] for i in range(len(target)))
    #             if word2 == target or word2 == target_backwards:
    #                 num_xmas += 1
    #         elif word == target_backwards:
    #             num_xmas += 1
    
    logger.info(f"Number of Xmas: {num_xmas}")

if __name__ == "__main__":
    day4_star1()