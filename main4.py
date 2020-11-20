from read_data import read_data
import copy
import numpy as np


def check_satisfy_constraint(group, group_tag, constraint, idx):

    if len(constraint) == 0:
        return True

    for i, tag_i in enumerate(group_tag):
        for tag_j in group_tag[i+1:]:
            if (tag_i is None) or (tag_j is None):
                continue
            if tag_i == tag_j:
                return False

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
                else:
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

def print_schedule(groups, timetable, processing):

    span = [0 for _ in groups]
    str_g = ["" for _ in groups]

    for g_idx, group in enumerate(groups):
        for idx, group_elem in enumerate(group):
            span[g_idx] += processing[group_elem]
            str_g[g_idx] += str(processing[group_elem]) + "-"
            if idx < len(group) - 1:
                span[g_idx] += timetable[group[idx]][group[idx + 1]]
                str_g[g_idx] += str(timetable[group[idx]][group[idx + 1]]) + "-"

    str_g = [str_g_elem[:-1] for str_g_elem in str_g]
    return span, str_g


def remove_inter_group(groups, timetable):

    n = len(groups)
    for i in range(n):
        for j in range(n):
            timetable[groups[i][-1]][groups[j][0]] = 9999

    return timetable


if __name__ == "__main__":
    data = read_data(10)

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

        # print(temp_timetable)

        for idx in range(data['n']):
            temp_timetable[from_job][idx] = 9999
            temp_timetable[idx][to_job] = 9999

        print(from_job, "->", to_job)

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
    tt_timetable = temp_timetable.copy()
    before_state[0] = temp_timetable.copy()

    group_set = set.union(*[set(g) for g in group])
    constraint_job = set(data['constraint'].keys())
    all_job = set(range(data['n']))

    print("all job          :", all_job)
    print("constraint job   :", constraint_job)
    print("group set        :", group_set)

    print("to do  : ", constraint_job - group_set)
    print("remove : ", (all_job - group_set) - constraint_job)
    remove_job = list((all_job - group_set) - constraint_job)
    todo_job = constraint_job - group_set

    for i in range(data['n']):
        for job in remove_job:
            temp_timetable[i][job] = 9999
            temp_timetable[job][i] = 9999

    print(temp_timetable)
    print("-----------------")

    heads, tails = [], []
    for i in range(data['m']):
        heads.append(group[i][0])
        tails.append(group[i][-1])

    cnt = 0
    while len(constraint_job - group_set) != 0:

        min_idx = temp_timetable.argmin()
        from_job, to_job = int(min_idx / data['n']), min_idx % data['n']
        print(from_job, to_job)

        group_idx = None
        case = None
        cur_job = None

        temp_group = copy.deepcopy(group)
        temp_group_tag = copy.deepcopy(group_tag)

        for i in range(data['m']):
            if from_job == tails[i]:
                temp_group[i].append(to_job)
                group_idx = i
                case = 1
                cur_job = to_job
            if to_job == heads[i]:
                temp_group[i].insert(0, from_job)
                group_idx = i
                case = 2
                cur_job = from_job

        if case is None:
            temp_timetable[from_job][to_job] = 9999
            continue

        tag = should_be_tag(temp_group[group_idx], temp_group_tag[group_idx], data['constraint'], temp_group_tag)
        temp_group_tag[group_idx] = tag
        satisfy = check_satisfy_constraint(temp_group, temp_group_tag, data['constraint'], group_idx)

        print(satisfy)
        print(temp_group, temp_group_tag)
        print("--------------")

        if satisfy:
            group = copy.deepcopy(temp_group)
            group_tag = copy.deepcopy(temp_group_tag)

            if case == 1:
                temp_timetable[:, to_job] = 9999
            elif case == 2:
                temp_timetable[from_job, :] = 9999

        else:
            temp_timetable[from_job][to_job] = 9999

        cnt += 1

        group_set = set.union(*[set(g) for g in group])

    span = evaluate_schedule(group, data['timetable'], data['processing'])
    print(group)
    print(group_tag)
    print(span)

    temp_timetable = data['timetable'].copy()
    temp_timetable = remove_inter_group(group, temp_timetable)

    for g in group:
        for g_elem in g:
            if g_elem != g[-1]:
                temp_timetable[g_elem, :] = 9999
            if g_elem != g[0]:
                temp_timetable[:, g_elem] = 9999

    # print(temp_timetable)
    group_set = set.union(*[set(g) for g in group])
    all_job = set(range(data['n']))
    todo_job = list(all_job - group_set)
    print(todo_job)

    for j in todo_job:
        temp_timetable[j, :] += data['processing'][j]
        temp_timetable[:, j] += data['processing'][j]

    temp_timetable[temp_timetable > 9999] = 9999
    # temp_timetable = temp_timetable.astype(np.float32)
    # temp_timetable += np.random.random_sample((data['n'], data['n']))
    # print(temp_timetable)

    print(span)
    print(todo_job)
    print("------------phase 3--------")
    cnt = 0
    while len(group_set) < data['n']:

        span = evaluate_schedule(group, data['timetable'], data['processing'])
        print(span)
        arg_min = span.index(min(span))
        cand1, cand2 = group[arg_min][0], group[arg_min][-1]
        print(cand1, cand2)

        all_cand = np.concatenate([temp_timetable[:, cand1], temp_timetable[cand2, :]])
        print(all_cand)
        print(all_cand.min())
        if all_cand.argmin()/data['n'] < 1:
            print(all_cand.argmin(), cand1)
            from_job, to_job = int(all_cand.argmin()), int(cand1)
        else:
            print(cand2, all_cand.argmin() - data['n'])
            from_job, to_job = int(cand2), int(all_cand.argmin() - data['n'])

        # from_job, to_job = np.where(temp_timetable == all_cand.min())
        # from_job, to_job = int(from_job[0]), int(to_job[0])
        print(from_job, to_job)

        if cand1 == to_job:
            group[arg_min].insert(0, from_job)
            temp_timetable[from_job, :] = 9999
            temp_timetable[:, group[arg_min][1]] = 9999
            print("case1!!")
        elif cand2 == from_job:
            group[arg_min].append(to_job)
            temp_timetable[:, to_job] = 9999
            temp_timetable[group[arg_min][-2], :] = 9999
            print("case2!!")

        print(group)
        print("-----------")
        group_set = set.union(*[set(g) for g in group])
        temp_timetable = remove_inter_group(group, temp_timetable)

        cnt += 1
        # if cnt == 1:
        #     break

    print(group)
    print(group_tag)
    span = evaluate_schedule(group, data['timetable'], data['processing'])
    print(span)
    print(data['processing'])
    print(sum(data['processing'])/data['m'])


    span, str_g = print_schedule(group, data['timetable'], data['processing'])
    for str_g_elem in str_g:
        print(str_g_elem)

    print(data['timetable'][28][25])


