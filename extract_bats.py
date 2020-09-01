from shutil import copy
import os
from os.path import isfile, isdir

from global_init import get_paths


paths = get_paths()


def check_folder_exists():
    if not isdir('bat_files'):
        os.mkdir('bat_files')


def run_script():

    check_folder_exists()

    for path in paths:
        source = f"./{path}/exec.bat"
        destination = f"./bat_files/{path}.bat"

        copy(source, destination)


if __name__ == "__main__":
    run_script()
