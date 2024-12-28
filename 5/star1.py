from prefect import flow, task, get_run_logger

def check_against_rule(rule: list, update: list) -> bool:
    before_page = rule[0]
    after_page = rule[1]
    
    before_index = None
    after_index = None

    for i in range(len(update)):
        if update[i] == before_page:
            before_index = i
        elif update[i] == after_page:
            after_index = i

    if before_index and after_index:
        if before_index > after_index:
            return False
    
    return True


@task
def read_page_orders():
    list1 = []
    with open("page_orderings.txt", "r") as file:
        for line in file:
            page1, page2 = line.strip().split("|")
            list1.append([page1, page2])
    return list1

@task
def read_updates():
    list1 = []
    with open("updates.txt") as file:
        for line in file:
            list1.append(line.strip().split(","))
    return list1

@flow
def page_updates():
    logger = get_run_logger()
    page_rules = read_page_orders()
    updates = read_updates()
    valid_updates = []

    for update in updates:
        valid_update = True
        for rule in page_rules:
            if rule[0] in update and rule[1] in update:
                if not check_against_rule(rule, update):
                    valid_update = False
                    break
        if valid_update:
            valid_updates.append(update)

    total = 0
    for valid_update in valid_updates:
        middle_index = int((len(valid_update)-1)/2)
        total += float(valid_update[middle_index])

    logger.info(f"Total: {total}")
            

if __name__ == "__main__":
    page_updates()