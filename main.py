from read_data import read_data
import copy


def check_satisfy_constraint(group, group_tag, constraint, idx):

    if len(constraint) == 0:
        return True

    for i, tag_i in enumerate(group_tag):
        for tag_j in group_tag[i+1:]:
            if tag_i == tag_j:
                return False

    if group_tag[idx]:
        for group_elem in group[idx]:
            if group_elem in constraint.keys():
                if not group_tag[idx] in constraint[group_elem]:
                    return False

    return True


def should_be_tag(group, tag, constraint):

    if len(constraint) == 0:
        return None

    if tag:
        return None

    for group_elem in group:
        if group_elem in constraint.keys():
            if len(constraint[group_elem]) == 1:
                return constraint[group_elem][0]

    return None


if __name__ == "__main__":
    data = read_data(6)

    print(data['constraint'])
    # data['constraint'][3] = [0]

    temp_timetable = data['timetable'].copy()

    group = [[] for _ in range(data['m'])]
    group_tag = [None for _ in range(data['m'])]
    print(group)

    before_state = [temp_timetable.copy(), copy.deepcopy(group), copy.deepcopy(group_tag)]

    print("------------------------")

    # set starting edge
    i = 0
    cnt = 0
    while i < data['m']:

        min_idx = temp_timetable.argmin()
        from_job, to_job = int(min_idx / data['n']), min_idx % data['n']

        print(temp_timetable)

        for idx in range(data['n']):
            temp_timetable[from_job][idx] = 9999
            temp_timetable[idx][to_job] = 9999

        print(from_job, to_job)

        group[i].append(from_job)
        group[i].append(to_job)

        tag = should_be_tag(group[i], group_tag[i], data['constraint'])
        group_tag[i] = tag

        satisfy = check_satisfy_constraint(group, group_tag, data['constraint'], i)

        if satisfy:
            i += 1
            before_state = [temp_timetable.copy(), copy.deepcopy(group), copy.deepcopy(group_tag)]
            print("it satisfy.. add edge !")
        else:
            temp_timetable = before_state[0].copy()
            group = copy.deepcopy(before_state[1])
            group_tag = copy.deepcopy(before_state[2])

            temp_timetable[from_job][to_job] = 9999
            before_state = [temp_timetable.copy(), copy.deepcopy(group), copy.deepcopy(group_tag)]
            print("it doesn't satisfy.. ")

        print("group.. : ", group)
        print("group tag : ", group_tag)
        print("constraint : ", satisfy)
        print("------------------------")

        cnt += 1

        if cnt == 10:
            break

    print(i)
    print(data['timetable'].argmin())