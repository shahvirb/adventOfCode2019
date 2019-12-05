import os
import pathlib

BASE_DIR = r"inputs"


def read(input=None):
    if not input:
        import inspect

        caller_filename = inspect.stack()[-1][0].f_code.co_filename
        caller_path = pathlib.Path(caller_filename)
        input = caller_path.stem + ".txt"

    return readfile(os.path.join(BASE_DIR, input))


def readfile(path):
    with open(path, "r") as file:
        return file.read()
