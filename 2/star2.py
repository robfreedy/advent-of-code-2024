from prefect import flow, task, get_run_logger

@task
def read_input():
    list1 = []
    with open("input.txt", "r") as file:
        for line in file:
            list1.append(line)
    return list1


def is_safe(nums):
    increasing = None
    for i in range(0, len(nums)):
        if i == 0:
            continue

        previousLevel = float(nums[i - 1])
        currentLevel = float(nums[i])

        score = currentLevel - previousLevel
        if score < -3 or score > 3 or score == 0:
            return False
        if increasing and score < 0:
            return False
        if increasing and score > 0:
            return False
        
        if score < 0:
            increasing = False
        else: 
            increasing = True
        
    return True

@flow
def safe_reports():
    logger = get_run_logger()
    reports = read_input()
    total = 0
    for report in reports:
        nums = report.split()
        if is_safe(nums):
            total += 1
        else:
            for i in range(0, len(nums)):
                numsCopy = nums.copy()
                numsCopy.pop(i)
                if is_safe(numsCopy):
                    total += 1
                    break
    logger.info(f"Total: {total}")

if __name__ == "__main__":
    safe_reports()