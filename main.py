from read_data import read_data


def check_satisfy_constraint(group, group_tag, constraint):
    pass

def constraint_reverse(constraint):

    job_constraint = {}

    for key in constraint.keys():
        for val in constraint[key]:

            if val in job_constraint.keys():
                job_constraint[val].append(key)
            else:
                job_constraint[val] = [key]

    return job_constraint


if __name__ == "__main__":
    data = read_data(8)

    job_constraint = constraint_reverse(data['constraint'])
    print(job_constraint)
    print(data)

    temp_timetable = data['timetable'].copy()

    group = [[] for _ in range(data['m'])]
    group_tag = [None for _ in range(data['m'])]
    print(group)

    # set starting edge
    for i in range(data['m']):

        min_idx = temp_timetable.argmin()
        from_job, to_job = int(min_idx / data['n']), min_idx % data['n']

        for idx in range(data['n']):
            temp_timetable[from_job][idx] = 9999
            temp_timetable[idx][to_job] = 9999
        print(temp_timetable)

        print(from_job, to_job)

        group[i].append(from_job)
        group[i].append(to_job)

        # check_job_constraint()

        print("group.. : ", group)
        print("group tag : ", group_tag)

    print(data['timetable'].argmin())