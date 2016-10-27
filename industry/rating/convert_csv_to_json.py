import argparse
import json
from tabulate import tabulate
import pandas
import numpy as np
import os
from collections import defaultdict


def student_2_tuple(name):
    return tuple(sorted([x for x in name.split(' ') if x != '']))


def all_students(path):
    with open(path, 'r') as f:
        students = json.load(f)
    res = {
        student_2_tuple(s): s
        for s in students
    }
    return res


def csv_table(path):
    return pandas.read_csv(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build markdown from jsons')
    parser.add_argument('--all-students', type=all_students, required=True,
                        help='path to json with all students')
    parser.add_argument('--input', type=csv_table, required=True,
                        help='csv table where first column is name and the others are marks')
    parser.add_argument('--output', type=str, required=True,
                        help='Target path')
    args = parser.parse_args()
    res = [
        {
            'identity': args.all_students[student_2_tuple(obj[0].encode('utf-8'))],
            'tasks': {
                args.input.columns[i]: obj[i]
                for i in xrange(1, len(obj))
            }
        }
        for _, obj in args.input.iterrows()
    ]
    with open(args.output, 'w') as f:
        json.dump(res, f, indent=4)
