import os
import os.path
import filecmp
from glob import glob
from pathlib import Path
from shutil import copyfile
import io
from file_functions import *
from line_ending_changer import *

new_engine_string = "UnrealEngine_experiment"
old_engine_string = "oldUE"
dev_engine_string = "D:\Perforce\TestInPlaceMerge"
output_string = "D:\Perforce\TestInPlaceMerge"
to_merge_string = "to_merge4"

# use this option if your engines are using LF while the dev branch is using CRLF, takes some time to run though
fix_engine_line_endings = False

differing_files = []
added_from_engine = []
added_from_dev = []

found_files = {""}

def engine_merge(file):
   in_old_string = get_corresponding_path(file, new_engine_string, old_engine_string)
   out_string = get_corresponding_path(file, new_engine_string, output_string)
   dev_string = get_corresponding_path(file, new_engine_string, dev_engine_string)
   merge_string =  get_corresponding_path(file, new_engine_string, to_merge_string)
   
   new_path = Path(file)
   old_path = Path(in_old_string)
   if not new_path.is_file():
      return
   
   elif not old_path.is_file():
        # the file doesn't exist in the old version, add it
        add_file(file, out_string)
        added_from_engine.append(file)
   elif cmp_file(in_old_string, file):
        # old and new engine file are the same
        if (Path(dev_string).is_file()):
           # we can use our own file since the old and new engine are the same, and if it doesn't exist in our engine we can ignore it
           add_file(dev_string, out_string)      
   else:
        if (Path(dev_string).is_file() and (not cmp_file(in_old_string, dev_string))):
            # trouble, our own file is also different
            differing_files.append(file)
            add_file(dev_string, merge_string)
            
        add_file(file, out_string)
   
   found_files.add(get_corresponding_path(file, new_engine_string, ""))



def dev_merge(file):
   if not (get_corresponding_path(file, dev_engine_string, "") in found_files) and not Path(get_corresponding_path(file, dev_engine_string, old_engine_string)).is_file():
        # if we didn't have this file before, and it didn't exist in the old engine, add it
        try:
            add_file(file, get_corresponding_path(file, dev_engine_string, output_string))
            added_from_dev.append(file)
        except PermissionError:
            print("error adding: " + file)



# here is where the program actually executes

if (fix_engine_line_endings):
    print("Fixing line endings...")
    execute_for_all_files(old_engine_string, convert_line_ending)
    execute_for_all_files(new_engine_string, convert_line_ending)

print ("Going through engine files...")
execute_for_all_files(new_engine_string, engine_merge)
print ("Going through dev files...")
execute_for_all_files(dev_engine_string, dev_merge)

added_engine_file = open("added_from_engine.txt", "w")
added_engine_file.write(str(added_from_engine).replace(",", "\n"))
added_dev_file = open("added_from_dev.txt", "w")
added_dev_file.write(str(added_from_dev).replace(",", "\n"))
differing_file = open("differing_files.txt", 'w')
differing_file.write(str(differing_files).replace(",", "\n"))

print("All done!")
