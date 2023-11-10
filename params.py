import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Arguments for GA_FJSP')
    parser.add_argument('--episode', type=int, default=1000001)
    parser.add_argument('--date', type=str, default=None)
    parser.add_argument('--detail', type=str, default="no")
    args = parser.parse_args()
    return args
