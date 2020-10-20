from read_data import read_data


def evaluate(time_table, processing, path):

    sum = 0
    n = len(path)
    for i in range(n-1):
        sum += processing[path[i]]
        sum += time_table[path[i]][path[i+1]]
    sum += processing[path[-1]]
    return sum


if __name__ == "__main__":
    data = read_data(1)
    time = evaluate(data['timetable'], data['processing'], [1-1, 2-1, 3-1])

    print("machine          :", data['m'])
    print("job              :", data['n'])
    print("processing time  :", data['processing'])
    print("timetable")
    print(data['timetable'])

    print("all time :", time)