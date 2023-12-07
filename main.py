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
        self.population_num = 2

        return

    def load_instance(self, filename):
        self.all_op_options, self.job_num, self.machine_num = load_instance(filename)

        for job in self.all_op_options:
            print(job)

    def initial_population(self):
        # raise "not yet"
        for _ in range(self.population_num):
            self.populations.append(random_init(self.all_op_options, self.job_num))
    def fitness_evaluation(self, process):
        # raise "not yet"
        # make sure the process satisfy the job precedent constrain

        # calculate makespan
        job_current_loading = [0] * self.job_num
        machine_current_loading = [0] * self.machine_num

        # for checking
        job_current_op = [0] * self.job_num

        for p in process:
            job_current_loading[p[0]] = max(job_current_loading[p[0]], machine_current_loading[p[2]]) + self.all_op_options[p[0]][p[1]][p[2]]
            machine_current_loading[p[2]] = job_current_loading[p[0]]
            
            # for check
            if job_current_op[p[0]] != p[1]:
                print("Wrong order")
            
            if self.all_op_options[p[0]][p[1]][p[2]] <= 0:
                print("Wrong assignment")
            
            job_current_op[p[0]] += 1

            # print('job {} on machine {} with process time : {}'.format(p[0], p[2], self.all_op_options[p[0]][p[1]][p[2]]))

            # print(job_current_loading)
            # print(machine_current_loading)
            # print('-'*50)
        
        print(process)
        print(machine_current_loading)
        return np.max(machine_current_loading)
        
    def selection(self):
        raise "not yet"
    def crossover(self, gene1, gene2):
        cross_point = random.randint(1, len(gene1) - 1)
        print(cross_point)
        child1, child2 = [], []
        job_current_op_1 = [0] * self.job_num
        job_current_op_2 = [0] * self.job_num

        #
        for i in range(cross_point):
            child1.append(gene1[i])
            child2.append(gene2[i])
            # check
            if job_current_op_1[gene1[i][0]] != gene1[i][1]:
                print("wrong")
            if job_current_op_2[gene2[i][0]] != gene2[i][1]:
                print("wrong")
            job_current_op_1[gene1[i][0]] += 1
            job_current_op_2[gene2[i][0]] += 1

        for i in range(len(gene1)):
            if job_current_op_1[gene2[i][0]] <= gene2[i][1]:
                child1.append(gene2[i])
                job_current_op_1[gene2[i][0]] += 1

            if job_current_op_2[gene1[i][0]] <= gene1[i][1]:
                child2.append(gene1[i])
                job_current_op_2[gene1[i][0]] += 1

        return child1, child2
    def mutation(self):
        



        raise "not yet"
    def stop_critetion(self):
        raise "not yet"


def main():
    env = GA_FJSP()
    env.load_instance('./datasets/FJSP/Brandimarte_Data/Mk00.fjs')
    env.initial_population()
    env.fitness_evaluation(env.populations[0])
    env.fitness_evaluation(env.populations[1])
    env.crossover(env.populations[0], env.populations[1])


if __name__ == '__main__':
    main()
    