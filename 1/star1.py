from prefect import flow, task, get_run_logger

@task
def read_input():
    list1 = []
    list2 = []
    with open("input.txt", "r") as file:
        for line in file:
            numbers = line.strip().split()
            list1.append(float(numbers[0]))
            list2.append(float(numbers[1]))
    return list1, list2

@flow
def find_distance_between_smallest() -> float:

    list1, list2 = read_input()

    if len(list1) < 1 or len(list2) < 1 or len(list1) != len(list2):
        raise ValueError("Both lists must contain at least two numbers.")
    
    list1 = sorted(list1)
    list2 = sorted(list2)

    logger = get_run_logger()
    
    total = 0

    for i in range(len(list1)):
        distance = abs(list1[i]-list2[i])
        total += distance

    logger.info(f"total: {total}")
    return total

if __name__ == "__main__":
    total_distance = find_distance_between_smallest()