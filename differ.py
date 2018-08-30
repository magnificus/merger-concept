import os
import os.path
import filecmp
from glob import glob
from pathlib import Path
from shutil import copyfile
import io
from file_functions import *

new_engine_string = "D:/Perforce/tbe_TJCGWS024_TestMergeScript_5802"
old_engine_string = "test"
dev_engine_string = "D:/Perforce/tbe_TJCGWS024_8612"
output_string = "testput"
to_merge_string = "to_merge3"


differing_files = []
added_from_engine = []
added_from_dev = []

found_files = {""}
new_engine_files = recursive_glob(new_engine_string)     

count = 0
numfiles = len(new_engine_files)

windows_line_ending = '\r\n'.encode()
linux_line_ending = '\n'.encode()


def merge():
    print (count)

print ("Going through engine files...")
for file in new_engine_files:
   in_old_string = get_corresponding_path(file, new_engine_string, old_engine_string)
   out_string = get_corresponding_path(file, new_engine_string, output_string)
   dev_string = get_corresponding_path(file, new_engine_string, dev_engine_string)
   merge_string =  get_corresponding_path(file, new_engine_string, to_merge_string)
   
   new_path = Path(file)
   old_path = Path(in_old_string)
   if not new_path.is_file():
      continue
   
   elif not old_path.is_file():
        # the file doesn't exist in the old version, add it
        hard_add_file(file, out_string)
        added_from_engine.append(file)
   elif cmp_file(in_old_string, file):
        # old and new engine file are the same
        if (Path(dev_string).is_file()):
           # we can use our own file since the old and new engine are the same, and if it doesn't exist we can ignore it
           hard_add_file(dev_string, out_string)      
   else:
        if (Path(dev_string).is_file() and (not cmp_file(in_old_string, dev_string))):
            # trouble, our own file is also different
            differing_files.append(file)
            hard_add_file(dev_string, merge_string)
            
        hard_add_file(file, out_string)
   
   found_files.add(get_corresponding_path(file, new_engine_string, ""))
   count += 1
   if ((count % 1000) == 0):
       print("worked through " + str(count) + " of " + str(numfiles) + " files")

dev_files = recursive_glob(dev_engine_string)


count = 0;
numfiles = len(dev_files)

print("Going through dev files...")
for file in dev_files:
   if not (get_corresponding_path(file, dev_engine_string, "") in found_files) and not Path(get_corresponding_path(file, dev_engine_string, old_engine_string)).is_file():
        # if we didn't have this file before, and it didn't exist in the old engine, add it
        try:
            hard_add_file(file, get_corresponding_path(file, dev_engine_string, output_string))
            added_from_dev.append(file)
        except PermissionError:
            print("error adding: " + file)
   count += 1
   if (count % 1000 == 0):
       print("worked through " + str(count) + " of " + str(numfiles) + " files")

added_engine_file = open("added_from_engine.txt", "w")
added_engine_file.write(str(added_from_engine).replace(",", "\n"))
added_dev_file = open("added_from_dev.txt", "w")
added_dev_file.write(str(added_from_dev).replace(",", "\n"))
differing_file = open("differing_files.txt", 'w')
differing_file.write(str(differing_files).replace(",", "\n"))

print("All done!")
