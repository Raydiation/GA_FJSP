import numpy as np
import os
import random
from params import get_args
import time
from utils import *
import functools

MAX = float(1e6)

def cmp(a, b):
    if a.fit_value > b.fit_value:
        return 1
    else:
        return -1

class GENE:
    def __init__(self, gene):
        self.gene = gene
        self.op_finish_time = []
        self.fit_value = -1
        self.max_load_machine = -1

    def h_clear(self): # to avoid something wrong
        self.op_finish_time = []
        self.fit_value = -1
        self.max_load_machine = -1

class GA_FJSP:
    def __init__(self, pop_num, child_num):
        self.all_op_options = []
        self.populations = []

        self.job_num = 0
        self.machine_num = 0

        # some hyperparameter
        self.population_num = pop_num
        self.gen_child_num = child_num

    def load_instance(self, filename):
        self.all_op_options, self.job_num, self.machine_num = load_instance(filename)

    def initial_population(self):
        for _ in range(self.population_num):
            random_gene = GENE(random_init(self.all_op_options, self.job_num))
            self.fitness_evaluation(random_gene)
            self.populations.append(random_gene)

    def gen(self):

        index = np.array([i for i in range(self.population_num)])
        prob = np.array([gene.fit_value for gene in self.populations])
        prob = prob / sum(prob)

        children = []

        # for _ in range(self.gen_child_num):
        for _ in range(self.gen_child_num):
            choice = np.random.choice(index, size=2, replace=False, p=prob)

            child1, child2 = self.crossover(self.populations[choice[0]], self.populations[choice[1]])
            self.fitness_evaluation(child1)
            self.fitness_evaluation(child2)

            self.mutation(child1)
            self.mutation(child2)

            self.fitness_evaluation(child1)
            self.fitness_evaluation(child2)
            children.append(child1)
            children.append(child2)

        # selection

        self.populations.extend(children)
        self.populations.sort(key=functools.cmp_to_key(cmp))
        del self.populations[self.population_num:]

    def fitness_evaluation(self, gene):
        # make sure the process satisfy the job precedent constrain

        # calculate makespan
        job_current_loading = [0] * self.job_num
        machine_current_loading = [0] * self.machine_num

        # for checking
        job_current_op = [0] * self.job_num

        for p in gene.gene:
            job_current_loading[p[0]] = max(job_current_loading[p[0]], machine_current_loading[p[2]]) + self.all_op_options[p[0]][p[1]][p[2]]
            machine_current_loading[p[2]] = job_current_loading[p[0]]
            gene.op_finish_time.append(job_current_loading[p[0]])
            
            # for check
            if job_current_op[p[0]] != p[1]:
                print("Wrong order")
            
            if self.all_op_options[p[0]][p[1]][p[2]] <= 0:
                print("Wrong assignment")
            
            job_current_op[p[0]] += 1
        
        gene.fit_value = np.max(machine_current_loading)
        gene.max_load_machine = np.argmax(machine_current_loading)
        return np.max(machine_current_loading)
        
    def crossover(self, gene1, gene2):
        cross_point = random.randint(1, len(gene1.gene) - 1)
        child1, child2 = GENE([]), GENE([])
        job_current_op_1 = [0] * self.job_num
        job_current_op_2 = [0] * self.job_num

        #
        for i in range(cross_point):
            child1.gene.append(gene1.gene[i])
            child2.gene.append(gene2.gene[i])
            # check
            if job_current_op_1[gene1.gene[i][0]] != gene1.gene[i][1]:
                print("wrong")
            if job_current_op_2[gene2.gene[i][0]] != gene2.gene[i][1]:
                print("wrong")
            job_current_op_1[gene1.gene[i][0]] += 1
            job_current_op_2[gene2.gene[i][0]] += 1

        for i in range(len(gene1.gene)):
            if job_current_op_1[gene2.gene[i][0]] <= gene2.gene[i][1]:
                child1.gene.append(gene2.gene[i])
                job_current_op_1[gene2.gene[i][0]] += 1

            if job_current_op_2[gene1.gene[i][0]] <= gene1.gene[i][1]:
                child2.gene.append(gene1.gene[i])
                job_current_op_2[gene1.gene[i][0]] += 1

        return child1, child2

    def mutation(self, gene):
        critical_path = [] # save the index of the operations on critical path
        current_finish_time = gene.fit_value
        max_load_job = -1
        max_load_machine = gene.max_load_machine

        # find critical path
        for i in range(len(gene.gene) - 1, -1, -1):
            if gene.op_finish_time[i] == current_finish_time:
                current_finish_time -= self.process_time(gene.gene[i])
                critical_path.append(i)
        critical_path.reverse()

        # mutation (change the selected machine)
        rng = random.randint(0, len(critical_path) - 1)
        new_machine = random.choice(np.where(np.array(self.all_op_options[gene.gene[critical_path[rng]][0]][gene.gene[critical_path[rng]][1]]) > 0)[0])
        new_ch = (gene.gene[critical_path[rng]][0], gene.gene[critical_path[rng]][1], new_machine) # an new chromosome
        gene.gene.pop(critical_path[rng])
        if new_ch[1] == 0: # op 0 of job_(new_ch[0])
            gene.gene.insert(0, new_ch)
        else:
            for i in range(len(gene.gene) - 1, -1, -1):
                if gene.gene[i][0] == new_ch[0] and gene.gene[i][1] == new_ch[1] - 1:
                    # insert at i + 1
                    gene.gene.insert(i + 1, new_ch)
                    break
        gene.h_clear()

    def process_time(self, ch):
        return self.all_op_options[ch[0]][ch[1]][ch[2]]

    def stop_critetion(self):
        raise "not yet"


def main():
    generation_num = 100
    env = GA_FJSP(10, 20)
    env.load_instance('./datasets/FJSP/Brandimarte_Data/Mk01.fjs')
    env.initial_population()
    for _ in range(generation_num):
        env.gen()
        print([gene.fit_value for gene in env.populations])


if __name__ == '__main__':
    main()
    