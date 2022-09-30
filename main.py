import re
import datetime
import matplotlib.pyplot as plt
import numpy as np


def parse_file_ifstat(file_name):
    file = open(file_name, "r")
    first_data = list()
    second_data = list()
    while True:
        line = file.readline()
        if not line:
            break
        line = line.strip()
        if re.match("^\d\d:\d\d:\d\d", line):
            columns = line.split()
            first_data.append(float(columns[1].replace(",", ".")))
            second_data.append(float(columns[2].replace(",", ".")))
    file.close()
    return first_data, second_data


def parse_file_iostat(file_name):
    file = open(file_name, "r")
    tps = list()
    kbs_read = list()
    kbs_write = list()
    while True:
        line = file.readline()
        if not line:
            break
        line = line.strip()
        if re.match("^(nvme0n1)", line):
            columns = line.split()
            if columns[0] == "nvme0n1":
                tps.append(float(columns[1].replace(",", ".")))
                kbs_read.append(float(columns[2].replace(",", ".")))
                kbs_write.append(float(columns[3].replace(",", ".")))
    file.close()
    return tps, kbs_read, kbs_write


def parse_file_pidstat(file_name):
    file = open(file_name, "r")
    usr = list()
    system = list()
    cpu = list()
    while True:
        line = file.readline()
        if not line:
            break
        line = line.strip()
        if re.match("^\d\d:\d\d:\d\d", line):
            columns = line.split()
            if columns[1] != "UID":
                usr.append(float(columns[3].replace(",", ".")))
                system.append(float(columns[4].replace(",", ".")))
                cpu.append(float(columns[7].replace(",", ".")))
    file.close()
    return usr, system, cpu


def parse_file_top(file_name):
    file = open(file_name, "r")

    pids = list()
    list_to_add = list()
    while True:
        line = file.readline()

        if not line:
            break

        line = line.strip()

        if re.match("^\d+", line):
            columns = line.split()
            list_to_add.append({int(columns[0]): columns[7]})
        elif re.match("(^PID)", line):
            if len(list_to_add) != 0:
                pids.append(list_to_add)
            list_to_add = list()

    if len(list_to_add) != 0:
        pids.append(list_to_add)

    file.close()
    return pids


def build_graph_to_ifstat(first_data, second_data):
    x = np.arange(0, len(first_data), 1)

    plt.grid()
    plt.xlabel("Время, с")
    plt.ylabel("KB/S_IN")
    plt.plot(x, first_data)
    plt.title("ifstat")
    plt.show()

    plt.grid()
    plt.xlabel("Время, с")
    plt.ylabel("KB/S_OUT")
    plt.plot(x, second_data)
    plt.title("ifstat")
    plt.show()


def build_graph_to_iostat(tps, kbs_read, kbs_write):
    x = np.arange(0, len(tps), 1)
    plt.xlabel("Время, с")

    plt.grid()
    plt.xlabel("Время, с")
    plt.ylabel("tps")
    plt.plot(x, tps)
    plt.title("iostat")
    plt.show()

    plt.grid()
    plt.xlabel("Время, с")
    plt.ylabel("KB/S_READ")
    plt.plot(x, kbs_read)
    plt.title("iostat")
    plt.show()

    plt.grid()
    plt.xlabel("Время, с")
    plt.ylabel("KB/S_WRITE")
    plt.plot(x, kbs_write)
    plt.title("iostat")
    plt.show()


def build_graph_to_pidstat(usr, system, cpu):
    fig, ax = plt.subplots()
    x = np.arange(0, len(usr), 1)
    plt.xlabel("Время, с")
    plt.ylabel("CPU, %")
    plt.title("pidstat")
    plt.grid()
    ax.plot(x, usr, "blue", label="usr%")
    ax.plot(x, system, "green", label="system%")
    ax.plot(x, cpu, "red", label="cpu%")
    plt.legend(loc="upper right")
    plt.show()


def build_graph_to_top(pids):
    print()


def main():
    res1, res2 = parse_file_ifstat("ifstat.log")
    build_graph_to_ifstat(res1, res2)

    res1, res2, res3 = parse_file_iostat("iostat.log")
    build_graph_to_iostat(res1, res2, res3)

    res1, res2, res3 = parse_file_pidstat("pidstat.log")
    build_graph_to_pidstat(res1, res2, res3)

    res1 = parse_file_top("top.log")
    build_graph_to_top(res1)


if __name__ == '__main__':
    main()
