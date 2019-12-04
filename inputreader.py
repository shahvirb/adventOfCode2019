import os
import pathlib

BASE_DIR = r"inputs"


def readlines(input=None):
    if not input:
        import inspect

        caller_filename = inspect.stack()[-1][0].f_code.co_filename
        caller_path = pathlib.Path(caller_filename)
        input = caller_path.stem + ".txt"

    lines = readfile(os.path.join(BASE_DIR, input))
    return [l.strip() for l in lines]


def readfile(path):
    with open(path, "r") as file:
        return file.readlines()
