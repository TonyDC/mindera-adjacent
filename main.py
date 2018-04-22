import argparse
from solver import Solver

# parse arguments: filename width
parser = argparse.ArgumentParser(description='Find adjacent cells in a 2D matrix')
parser.add_argument('filename', metavar='file', action='store', type=str, help='path to file containing the matrix')

args = parser.parse_args()

try:
    solver = Solver(args.filename)
    solver.output_groups()
except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
