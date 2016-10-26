import argparse
import json
from tabulate import tabulate
import pandas
import numpy as np


def json_object(path):
    with open(path, 'r') as f:
        obj = json.load(f)
    return obj


def validate_config(config_obj):
    assert(type(config_obj) is dict)
    tasks = config_obj.get('task_identities')
    assert(type(tasks) is list)
    if tasks is None:
        print 'There is no task_identities in config'
        return False
    config_obj['task_lengths'] = [len(task) + 5 for task in tasks]
    tasks = set(tasks)
    
    # validate weights

    industry_weights = config_obj.get('industry_weights')
    assert(type(industry_weights) is dict)
    if industry_weights is None:
        print 'There is no industry_weights in config'
        return False
    for task, weight in industry_weights.iteritems():
        if task not in tasks:
            print "industry_weights's key '{}' is not found in tasks".format(task)
            return False

    sport_weights = config_obj.get('sport_weights')
    assert(type(sport_weights) is dict)
    if sport_weights is None:
        print 'There is no sport_weights in config'
        return False
    for task, weight in sport_weights.iteritems():
        if task not in tasks:
            print "sport_weights's key '{}' is not found in tasks".format(task)
            return False

    trends_weights = config_obj.get('trends_weights')
    assert(type(trends_weights) is dict)
    if trends_weights is None:
        print 'There is no trends_weights in config'
        return False
    for task, weight in trends_weights.iteritems():
        if task not in tasks:
            print "trends_weights's key '{}' is not found in tasks".format(task)
            return False

    return True


def validate_students(students, config_obj):
    tasks = set(config_obj['task_identities'])
    for student in students:
        assert(type(student) is dict)
        identity = student.get('identity')
        if identity is None:
            print 'There is no identity of some student'
            return False

        student['identity_tuple'] = tuple(sorted(filter(lambda x: len(x) > 0, identity.split(' '))))

        student_tasks = student.get("tasks", {})
        # validate student's tasks
        for task, score in student_tasks.iteritems():
            if task not in tasks:
                print "Student {} has unknown task - '{}'".format(identity, task)
                return False

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build markdown from jsons')
    parser.add_argument('--students', type=json_object, required=True,
                        help='Path to json with students (usually it is sudents.json)')
    parser.add_argument('--config', type=json_object, required=True,
                        help='Path to json with table configuration (usually it is rating_config.json)')
    parser.add_argument('--output', type=str, required=True,
                        help='Target path')
    args = parser.parse_args()

    if validate_config(args.config):
        if validate_students(args.students, args.config):
            df = {
                task: []
                for task in args.config['task_identities']
            }
            df['student'] = []
            for student in args.students:
                df['student'].append(student['identity'])
                student_tasks = student.get("tasks", {})

                for task, length in zip(args.config['task_identities'], args.config['task_lengths']):
                    df[task].append(student_tasks.get(task, 0))

            df = pandas.DataFrame(df, columns=['student'] + args.config['task_identities']).sort_values(by='student')
            
            df['industry_result'] = np.zeros(len(df))
            for task, weight in args.config['industry_weights'].iteritems():
                df.industry_result += weight * df[task]

            df['sport_result'] = np.zeros(len(df))
            for task, weight in args.config['sport_weights'].iteritems():
                df.sport_result += weight * df[task]

            df['trends_result'] = np.zeros(len(df))
            for task, weight in args.config['trends_weights'].iteritems():
                df.trends_result += weight * df[task]

            with open(args.output, 'w') as f:
                f.write(tabulate(df, headers="keys", tablefmt="pipe").encode('utf-8') + '\n')
