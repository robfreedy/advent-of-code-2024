from prefect import flow, task, get_run_logger

@task
def read_input():
    list1 = []
    with open("input.txt", "r") as file:
        for line in file:
            list1.append(line)
    return list1

@flow
def safe_reports():
    logger = get_run_logger()
    reports = read_input()
    total = 0
    for report in reports:
        nums = report.split()
        safe = True
        if float(nums[0]) > float(nums[1]):
            for i in range(0, len(nums)-1):
                diff = float(nums[i]) - float(nums[i+1])
                if diff != 1 and diff != 2 and diff != 3:
                    safe = False
            if safe:
                total += 1
        elif float(nums[1]) > float(nums[0]):
            for i in range(0, len(nums)-1):
                diff = float(nums[i+1]) - float(nums[i])
                if diff != 1 and diff != 2 and diff != 3:
                    safe = False
            if safe:
                total += 1
    logger.info(f"Total: {total}")
    return total

if __name__ == "__main__":
    safe_reports()