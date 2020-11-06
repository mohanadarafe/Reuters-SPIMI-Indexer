
import argparse
import json
import sys
from os import path

def init_params():
    parser = argparse.ArgumentParser(description='Process input path parameter')
    parser.add_argument('-i', '--input_file', default=sys.stdin, help='Input from file, default stdin')  # all blocks
    parser.add_argument('-o', '--output_file', default=sys.stdout, help='Output to file, default stdout')  # all blocks
    parser.add_argument('-p', '--path', help='Reuters collection directory')  # block 1
    parser.add_argument('-q', '--query', nargs='*', default=None, help='Query')  # block 8
    init_params.args = parser.parse_args()

    if type(init_params.args.input_file) is str:
        common_check_path(init_params.args.input_file)
        init_params.args.input_file = open(init_params.args.input_file)

    if type(init_params.args.output_file) is str:
        init_params.args.output_file = open(init_params.args.output_file, 'w')

    return init_params.args


def common_check_path(file):
    assert path.exists(file), "input file does not exists"

def output(structure):
    print(json.dumps(structure), file=init_params.args.output_file)