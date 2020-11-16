
import argparse
import json
import sys
from os import path

def init_params():
    parser = argparse.ArgumentParser(description='Process input path parameter')
    parser.add_argument('-i', '--input_file', default=sys.stdin, help='Input from file, default stdin')  
    parser.add_argument('-o', '--output_file', default=sys.stdout, help='Output to file, default stdout')  
    parser.add_argument('-p', '--path', help='Reuters collection directory')  
    parser.add_argument('-q', '--query', nargs='*', default=None, help='Query') 
    parser.add_argument('-t', '--type', nargs='*', default=None, help='Query Type') 
    init_params.args = parser.parse_args()

    if type(init_params.args.input_file) is str:
        common_check_path(init_params.args.input_file)
        init_params.args.input_file = open(init_params.args.input_file)

    return init_params.args


def common_check_path(file):
    assert path.exists(file), "input file does not exists"

def output(structure):
    print(json.dumps(structure), file=init_params.args.output_file)