
import os


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        raise RuntimeError("Error: Creating directory. " + directory)


def isfileexists(filepath):
    return os.path.isfile(filepath)
