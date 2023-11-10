import random
import time
import numpy as np
from params import get_args

def heuristic_init(all_op_options):
    job_progress_idx = [0] * len(all_op_options)
    job_progress_time = [0] * len(all_op_options)

    while True:

        p = random.rand()


def load_instance(filename):
    all_op_options = []
    f = open(filename)
    line = f.readline().split()
    job_num, machine_num = int(line[0]), int(line[1])

    for i in range(job_num):
        line = f.readline().split()
        op_num = int(line[0])
        cur = 1
        this_job = []
        for j in range(op_num):
            this_op_options = [0] * machine_num
            options_num = int(line[cur])
            cur += 1
            for _ in range(options_num):
                machine_id, process_time = int(line[cur]) - 1, int(line[cur + 1])
                this_op_options[machine_id] = process_time
                cur += 2
            this_job.append(this_op_options)
        all_op_options.append(this_job)

    for job in all_op_options:
        print(job)

    print(len(all_op_options))

    return all_op_options

if __name__ == '__main__':
    args = get_args()
    load_instance('./datasets/FJSP/Brandimarte_Data/Mk01.fjs')