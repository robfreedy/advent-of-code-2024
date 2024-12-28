from prefect import flow, task, get_run_logger

#### Needed some help from Reddit on this one

def kahn_sort(sequence, rules):
    in_degrees = {}
    if len(sequence) == 1:
        return sequence
    for number in sequence:
        in_degrees[number] = 0
        for rule in rules:
            if rule[1] == number:
                in_degrees[number] += 1
        if in_degrees[number] == 0:
            new_seq = [x for x in sequence]
            new_seq.remove(number)
            new_rules = [x for x in rules]
            for rule in rules:
                if rule[0] == number:
                    new_rules.remove(rule)
            sorted_list = kahn_sort(new_seq, new_rules)
            if sorted_list is not False:
                return [number] + sorted_list
    return False


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

    associated_rules = {}
    for sequence in updates:
        for rule in page_rules:
            if all(ele in sequence for ele in rule):
                if associated_rules.get(tuple(sequence)) == None:
                    associated_rules[tuple(sequence)] = []
                associated_rules[tuple(sequence)].append(rule)
    
    correct_sum = 0
    fixed_sum = 0
    for sequence in updates:
        result = kahn_sort(sequence, associated_rules[tuple(sequence)])
        if result != sequence:
            fixed_sum += int(result[len(result) // 2])
        else:
            correct_sum += int(result[len(result) // 2])

    logger.info(f"Sum of fixed sequences: {fixed_sum}")
            

if __name__ == "__main__":
    page_updates()