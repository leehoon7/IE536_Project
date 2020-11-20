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

    print(constraint)
    print(group, group_tag)
    if not (group_tag[idx] is None):
        for group_elem in group[idx]:
            if group_elem in constraint.keys():
                if not group_tag[idx] in constraint[group_elem]:
                    return False

    all_num = sum([len(g) for g in group])
    group_set = set.union(*[set(g) for g in group])

    if all_num != len(group_set):
        return False

    return True


def should_be_tag(group, tag, constraint, group_tag):

    if len(constraint) == 0:
        return None

    if not (tag is None):
        return tag

    for group_elem in group:
        if group_elem in constraint.keys():
            if len(constraint[group_elem]) == 1:
                return constraint[group_elem][0]
            elif len(constraint[group_elem]) == 2:
                temp = list(set(constraint[group_elem]) - set(group_tag))
                if len(temp) == 1:
                    return temp[0]

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
            timetable[groups[i][-1]][groups[j][0]] = 9999

    return timetable


if __name__ == "__main__":
    data = read_data(8)

    print(data['constraint'])
    constraint_job = list(data['constraint'].keys())
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

        tag = should_be_tag(group[i], group_tag[i], data['constraint'], group_tag)
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

    # print(i)
    span = evaluate_schedule(group, data['timetable'], data['processing'])
    print(span)

    num_in_group = sum([len(g) for g in group])
    # print(num_in_group)
    # print(temp_timetable)

    # different group eliminate..
    temp_timetable = remove_inter_group(group, temp_timetable)
    before_state[0] = temp_timetable.copy()

    # print(temp_timetable)
    cnt = 0
    while num_in_group < data['n']:

        if len(set(constraint_job)) == 0:
            break

        tt_timetable = temp_timetable.copy()
        heads, tails = [], []
        for i in range(data['m']):
            heads.append(group[i][0])
            tails.append(group[i][-1])

        # remove all col without head.
        for i in range(data['n']):
            if not (i in heads):
                tt_timetable[:, i] = 9999
        # print(temp_timetable)
        # restore row correlated with tail.
        for i in range(data['n']):
            if i in tails:
                tt_timetable[i] = before_state[0][i]

        print(temp_timetable)
        print(tt_timetable)
        min_idx = tt_timetable.argmin()
        print(min_idx)
        from_job, to_job = int(min_idx / data['n']), min_idx % data['n']
        #
        print(from_job, to_job)

        group_idx = None
        case = None
        cur_job = None
        for i in range(data['m']):
            if from_job == tails[i]:
                group[i].append(to_job)
                group_idx = i
                case = 1
                cur_job = to_job
            if to_job == heads[i]:
                group[i].insert(0, from_job)
                group_idx = i
                case = 2
                cur_job = from_job

        print(group)
        print(group_tag)
        print(group_idx)
        tag = should_be_tag(group[group_idx], group_tag[group_idx], data['constraint'], group_tag)
        group_tag[group_idx] = tag
        satisfy = check_satisfy_constraint(group, group_tag, data['constraint'], group_idx)

        print("current job  :", cur_job)

        if not (cur_job in constraint_job):
            satisfy = False

        print("group..      :", group)
        print("group tag    :", group_tag)
        print("constraint   :", satisfy)

        if satisfy:
            print("group : ", group)

            if case == 1:
                temp_timetable[:, to_job] = 9999
            elif case == 2:
                temp_timetable[from_job, :] = 9999

            temp_timetable = remove_inter_group(group, temp_timetable)

            before_state = [temp_timetable.copy(), copy.deepcopy(group), copy.deepcopy(group_tag)]
            print("it satisfy.. add edge !")

            group_set = set.union(*[set(g) for g in group])

            if len(set(constraint_job) - group_set) == 0:
                break

        else:
            group = copy.deepcopy(before_state[1])
            group_tag = copy.deepcopy(before_state[2])

            temp_timetable[from_job][to_job] = 9999
            before_state = [temp_timetable.copy(), copy.deepcopy(group), copy.deepcopy(group_tag)]
            print("it doesn't satisfy.. ")

        cnt += 1
        # if cnt == 20:
        #     break


        print("----------------------")

        num_in_group = sum([len(g) for g in group])

    print(temp_timetable, group, group_tag)

    span = evaluate_schedule(group, data['timetable'], data['processing'])
    print(span)

