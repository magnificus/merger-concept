import os
import os.path
import filecmp
from glob import glob
from pathlib import Path
from shutil import copyfile
import io

def recursive_glob(rootdir='.', suffix=''):
    return [os.path.join(looproot, filename)
            for looproot, _, filenames in os.walk(rootdir)
            for filename in filenames if filename.endswith(suffix)]          
            
def get_corresponding_path(file_name, current_dir, wanted_dir):
    return file_name.replace(current_dir, wanted_dir, 1)

def add_file(original_file, new_location):
    if (original_file == new_location):
        return
    if (os.path.exists(new_location)):
        os.remove(new_location)
    if (not os.path.exists(os.path.dirname(new_location))):
        os.makedirs(os.path.dirname(new_location))
    copyfile(original_file, new_location)

def cmp_file(path_1, path_2):
    return filecmp.cmp(path_1, path_2, shallow=False)


def execute_for_all_files(location, function):
    files = recursive_glob(location)
    count = 0
    numfiles = len(files)
    for file in files:
        function(file)
        count += 1
        if ((count % 500) == 0):
            print('%.1f'%(float(count)*100/float(numfiles)) + "%")
