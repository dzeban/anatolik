from os.path import splitext as splitext
from os.path import basename as basename
import os
import shutil

def name(path):
    """ Returns filename without path and extension """
    return splitext( basename(path) )[0]

def copy_dir(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
