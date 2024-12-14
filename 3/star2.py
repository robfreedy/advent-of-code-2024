from prefect import flow, get_run_logger, task
import re

@task
def multiply_numbers(mul_statement: str):
    nums = [int(s) for s in re.findall(r'\b\d+\b', mul_statement)]
    return nums[0] * nums[1]

@flow
def day3_star2():
    logger = get_run_logger()
    mult_list_of_lists = []
    pattern = r'mul\([0-9]{1,3}\,[0-9]{1,3}\)'
    do_pattern = r'do\(\)'
    dont_pattern = r'don\'t\(\)'
    with open("input.txt", "r") as file:
        i = 0
        file_string = ''
        for character in file.read():
            file_string += character

    split_line_by_first_dont = re.split(dont_pattern, file_string, 1)
    mult_list = [match.group(0) for match in re.finditer(pattern, split_line_by_first_dont[0])]
    mult_list_of_lists.append(mult_list)
    split_lines_by_dont = re.split(dont_pattern, split_line_by_first_dont[1])
    
    for line in split_lines_by_dont:
        mult_list = []
        if re.compile(do_pattern).search(line):
            split_line_by_do = re.split(do_pattern, line, 1)
            mult_list = [match.group(0) for match in re.finditer(pattern, split_line_by_do[1])]

        mult_list_of_lists.append(mult_list)

    result = 0
    for mult_list in mult_list_of_lists:
        for mult in mult_list:
            result += multiply_numbers(mult)

    logger.info(f"Result: {result}")

if __name__ == "__main__":
    day3_star2()