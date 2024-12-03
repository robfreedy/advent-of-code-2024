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
def generate_similarity_scores():

    logger = get_run_logger()

    list1, list2 = read_input()

    total = 0
    for i in list1:
        num = list2.count(i)
        sim_score = num*i
        total += sim_score

    logger.info(f"Total: {total}")

if __name__ == "__main__":
    total_distance = generate_similarity_scores()