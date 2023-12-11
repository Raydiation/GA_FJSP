import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Arguments for GA_FJSP')
    parser.add_argument('--population_num', type=int, default=100)
    parser.add_argument('--child_num', type=int, default=200)
    parser.add_argument('--generation_num', type=int, default=2000)
    parser.add_argument('--mutation_rate', type=float, default=0.25)
    parser.add_argument('--tabu_num', type=float, default=20000) # 0 -> not using tabu search
    
    parser.add_argument('--file_dir', type=str, default='./datasets/FJSP/Brandimarte_Data')
    # file dir options
    # file_dir = './datasets/FJSP/Brandimarte_Data'
    # file_dir = './datasets/FJSP/Hurink_Data/Text/edata'
    # file_dir = './datasets/FJSP/Hurink_Data/Text/rdata'
    # file_dir = './datasets/FJSP/Hurink_Data/Text/vdata'

    parser.add_argument('--date', type=str, default='DUMMY')
    args = parser.parse_args()
    return args
