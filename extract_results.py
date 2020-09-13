from shutil import copy, rmtree
import os
from os.path import isfile, isdir

from global_init import get_paths


paths = get_paths('Linux')


def check_folder_exists():
    if not isdir('results'):
        os.mkdir('results')


def remove_previous_contents():
    rmtree('results')


def run_script():

    remove_previous_contents()

    check_folder_exists()

    for path in paths:
        source = f"./{path}/results/results.csv"
        destination = f"./results/{path}_results.csv"

        copy(source, destination)


if __name__ == "__main__":
    run_script()
