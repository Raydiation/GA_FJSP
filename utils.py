import random
import time
import numpy as np
from params import get_args

def random_init(all_op_options, job_num):
    """
    process = [(i0, j0, k0), (i1, j1, k1) ... (it, jt, kt) ...]
    assert len(process) = total operation num

    p-th tuple (ip, jp, kp) means that the jp-th operation of ip-th job executed by kp-th machine
    """
    # for job in all_op_options:
    #     print(job)
    job_progress = np.zeros(job_num, dtype=int) 
    finish_job_num = 0
    process = []
    while finish_job_num < job_num:
        next_job = random.choice(np.where(job_progress >= 0)[0])
        select_m = random.choice(np.where(np.array(all_op_options[next_job])[job_progress[next_job]] > 0)[0])
        # print('next_job : {}'.format(next_job))
        # print('its progress : {}'.format(job_progress[next_job]))
        # print('this job : {}'.format(np.array(all_op_options[next_job])))
        # print('this op : {}'.format(np.array(all_op_options[next_job])[job_progress[next_job]]))
        # print('select machine : {}'.format(select_m))
        # print('-'*50)
        process.append((next_job, job_progress[next_job], select_m))

        job_progress[next_job] += 1
        if (job_progress[next_job] >= len(all_op_options[next_job])):
            job_progress[next_job] = -1
            finish_job_num += 1
    # for t in process:
    #     print('(job_id, op_id, machine_id) : {} process time : {}'.format(t, all_op_options[t[0]][t[1]][t[2]]))
    # print(len(process))
    return process

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

    # for job in all_op_options:
    #     print(job)

    return all_op_options, job_num, machine_num

if __name__ == '__main__':
    args = get_args()
    
    random_init(load_instance('./datasets/FJSP/Brandimarte_Data/Mk01.fjs'))