from prefect import flow, get_run_logger, task
import re

@task
def multiply_numbers(mul_statement: str):
    nums = [int(s) for s in re.findall(r'\b\d+\b', mul_statement)]
    return nums[0] * nums[1]

@flow
def day3_star1():
    logger = get_run_logger()
    mult_list = []
    pattern = r'mul\([0-9]{1,3}\,[0-9]{1,3}\)'
    with open("input.txt", "r") as file:
        mult_list = [match.group(0) for line in file for match in re.finditer(pattern, line)]

    result = 0
    for mult in mult_list:
        result += multiply_numbers(mult)

    logger.info(f"Result: {result}")

if __name__ == "__main__":
    day3_star1()