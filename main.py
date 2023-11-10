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

        # some hyperparameter
        self.population_num = 1

        return

    def load_instance(self, filename):
        self.all_op_options = load_instance(filename)

        for job in self.all_op_options:
            print(job)

    def initial_population(self):
        raise "not yet"
        random_init()
    def fitness_evaluation(self, his):
        raise "not yet"
        # calculate makespan
        
    def selection(self):
        raise "not yet"
    def offspring_gen(self):
        raise "not yet"
    def stop_critetion(self):
        raise "not yet"


def main():
    env = GA_FJSP()
    env.load_instance('./datasets/FJSP/Brandimarte_Data/Mk01.fjs')


if __name__ == '__main__':
    main()
    