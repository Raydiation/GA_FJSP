import numpy as np
import os
import random
from params import get_args
from torch.utils.tensorboard import SummaryWriter
import time
import copy
from utils import *

MAX = float(1e6)

class GA_FJSP:
    def __init__(self):
        self.all_op_options = []
        self.populations = []

        self.job_num = 0
        self.machine_num = 0

        # some hyperparameter
        self.population_num = 1

        return

    def load_instance(self, filename):
        self.all_op_options, self.job_num, self.machine_num = load_instance(filename)

        for job in self.all_op_options:
            print(job)

    def initial_population(self):
        # raise "not yet"
        self.populations.append(random_init(self.all_op_options, self.job_num))
    def fitness_evaluation(self, process):
        # raise "not yet"
        # make sure the process satisfy the job precedent constrain

        # calculate makespan
        job_current_loading = [0] * self.job_num
        machine_current_loading = [0] * self.machine_num

        for p in process:
            job_current_loading[p[0]] = max(job_current_loading[p[0]], machine_current_loading[p[2]]) + self.all_op_options[p[0]][p[1]][p[2]]
            machine_current_loading[p[2]] = job_current_loading[p[0]]
            # print('job {} on machine {} with process time : {}'.format(p[0], p[2], self.all_op_options[p[0]][p[1]][p[2]]))

            # print(job_current_loading)
            # print(machine_current_loading)
            # print('-'*50)
        

        return np.max(machine_current_loading)
        
    def selection(self):
        raise "not yet"
    def offspring_gen(self):
        raise "not yet"
    def stop_critetion(self):
        raise "not yet"


def main():
    env = GA_FJSP()
    env.load_instance('./datasets/FJSP/Brandimarte_Data/Mk01.fjs')
    env.initial_population()
    env.fitness_evaluation(env.populations[0])


if __name__ == '__main__':
    main()
    