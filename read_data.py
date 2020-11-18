import csv
import numpy as np


def read_data(file_name):

    file_name = 'data/data' + str(file_name) + '.txt'
    data = {}
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        # first part : instance number / number of machines (m) / number of jobs (n)
        row = next(reader)
        data['instance'] = int(row[0].split(' ')[-1])
        data['m'] = int(row[2].split('=')[-1])
        data['n'] = int(row[3].split('=')[-1])

        # second part : setup time table --> n * n
        row = next(reader)
        row = next(reader)  # for dummy line
        timetable = []
        for i in range(data['n']):
            row = next(reader)[1:]
            row[i] = 9999
            row = [int(time) for time in row]
            timetable.append(row)
        timetable = np.array(timetable)
        data['timetable'] = timetable

        # third part : processing time --> 1 * n
        row = next(reader)  # for dummy line
        row = next(reader)[1:]
        processing = [int(time) for time in row]
        data['processing'] = processing

        # fourth part : machine availability
        row = next(reader)  # for dummy line
        constraint = {}
        for row in reader:
            if row[0] == 'No machine availability constraints':
                break
            else:
                jobs = row[1][4:].split(',')
                jobs = [int(job) - 1 for job in jobs]

                machines = row[2][7:].split(',')
                machines = [int(machine) - 1 for machine in machines]

                for job in jobs:
                    for machine in machines:
                        if job in constraint.keys():
                            constraint[job].append(machine)
                        else:
                            constraint[job] = [machine]

        data['constraint'] = constraint

    return data


if __name__ == "__main__":
    data = read_data(2)

    print("instance         :", data['instance'])
    print("machine          :", data['m'])
    print("job              :", data['n'])
    print("processing time  :", data['processing'])
    print("timetable")
    print(data['timetable'])
    print("constraint")
    print(data['constraint'])