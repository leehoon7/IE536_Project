from read_data import read_data
import copy


def check_satisfy_constraint(group, group_tag, constraint, idx):

    if len(constraint) == 0:
        return True

    for i, tag_i in enumerate(group_tag):
        for tag_j in group_tag[i+1:]:
            if (tag_i is None) or (tag_j is None):
                continue
            if tag_i == tag_j:
                return False

    if group_tag[idx]:
        for group_elem in group[idx]:
            if group_elem in constraint.keys():
                if not group_tag[idx] in constraint[group_elem]:
                    return False

    all_num = sum([len(g) for g in group])
    group_set = set.union(*[set(g) for g in group])

    if all_num != len(group_set):
        return False

    return True


def should_be_tag(group, tag, constraint):

    if len(constraint) == 0:
        return None

    if not (tag is None):
        return tag

    for group_elem in group:
        if group_elem in constraint.keys():
            if len(constraint[group_elem]) == 1:
                return constraint[group_elem][0]

    return None


def evaluate_schedule(groups, timetable, processing):

    span = [0 for _ in groups]

    for g_idx, group in enumerate(groups):
        for idx, group_elem in enumerate(group):
            span[g_idx] += processing[group_elem]
            if idx < len(group) - 1:
                span[g_idx] += timetable[group[idx]][group[idx + 1]]

    return span


def remove_inter_group(groups, timetable):

    n = len(groups)
    for i in range(n):
        for j in range(n):
            # if i == j:
            #     continue
            print(groups[i][-1], groups[j][0])
            timetable[groups[i][-1]][groups[j][0]] = 9999

    return timetable


if __name__ == "__main__":
    data = read_data(2)

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

    print(i)
    span = evaluate_schedule(group, data['timetable'], data['processing'])
    print(span)

    num_in_group = sum([len(g) for g in group])
    print(num_in_group)
    print(temp_timetable)

    # different group eliminate..
    temp_timetable = remove_inter_group(group, temp_timetable)
    before_state[0] = temp_timetable.copy()

    print(temp_timetable)

    while num_in_group < data['n']:

        heads, tails = [], []
        for i in range(data['m']):
            heads.append(group[i][0])
            tails.append(group[i][-1])

        # remove all col without head.
        for i in range(data['n']):
            if not (i in heads):
                temp_timetable[:, i] = 9999
        print(temp_timetable)
        # restore row correlated with tail.
        for i in range(data['n']):
            if i in tails:
                temp_timetable[i] = before_state[0][i]

        print(temp_timetable)
        min_idx = temp_timetable.argmin()
        from_job, to_job = int(min_idx / data['n']), min_idx % data['n']
        #
        print(from_job, to_job)

        for i in range(data['m']):
            if from_job == tails[i]:
                group[i].append(to_job)
            if to_job == heads[i]:
                group[i].insert(0, from_job)

        print(group)

        break

