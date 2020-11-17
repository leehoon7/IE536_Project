import dgl
from read_data import read_data

if __name__ == "__main__":
    data = read_data(2)
    print(data)

    temp_timetable = data['timetable'].copy()

    

    for _ in range(data['m']):
        min_idx = temp_timetable.argmin()
        from_job, to_job = int(min_idx / data['n']), min_idx % data['n']

        for idx in range(data['n']):
            temp_timetable[from_job][idx] = 9999
            temp_timetable[idx][to_job] = 9999
        print(temp_timetable)

        print(from_job, to_job)

    print(data['timetable'].argmin())