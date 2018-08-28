import os
import filecmp
from glob import glob
from pathlib import Path
from shutil import copyfile

new_engine_string = "new_engine"
old_engine_string = "old_engine"
dev_engine_string = "main"
output_string = "output"

def recursive_glob(rootdir='.', suffix=''):
    return [os.path.join(looproot, filename)
            for looproot, _, filenames in os.walk(rootdir)
            for filename in filenames if filename.endswith(suffix)]          
            
def get_corresponding_path(file_name, current_dir, wanted_dir):
    return file_name.replace(current_dir, wanted_dir, 1)

def hard_add_file(original_file, new_location):
    if (os.path.exists(new_location)):
        os.remove(new_location)
    if (not os.path.exists(os.path.dirname(new_location))):
        os.makedirs(os.path.dirname(new_location))
    copyfile(original_file, new_location)

differing_files = []
added_from_engine = []
added_from_dev = []

found_files = {""}
new_engine_files = recursive_glob(new_engine_string)            
for file in new_engine_files:
   in_old_string = get_corresponding_path(file, new_engine_string, old_engine_string)
   out_string = get_corresponding_path(file, new_engine_string, output_string)
   dev_string = get_corresponding_path(file, new_engine_string, dev_engine_string)
   
   new_path = Path(file)
   old_path = Path(in_old_string)
   if not new_path.is_file():
      continue
   
   elif not old_path.is_file():
      # the file doesn't exist in the old version, add it
      hard_add_file(file, out_string)
      added_from_engine.append(file)
   elif filecmp.cmp(in_old_string, file):
       # old and new engine file are the same
       if (Path(dev_string).is_file()):
           # we can use our own file since the old and new engine are the same, and if it doesn't exist we can ignore it
           hard_add_file(dev_string, out_string)      
   else:
        # uh oh new and old engine are different
        if (Path(dev_string).is_file() and (not filecmp.cmp(in_old_string, dev_string))):
            # trouble, our own file is also different
            differing_files.append(file)
            
        hard_add_file(file, out_string)
   
   found_files.add(get_corresponding_path(file, new_engine_string, ""))

dev_files = recursive_glob(dev_engine_string)

for file in dev_files:
    if ( not (get_corresponding_path(file, dev_engine_string, "") in found_files)):
        # if we didn't have this file, add it
        hard_add_file(file, get_corresponding_path(file, dev_engine_string, output_string))
        added_from_dev.append(file)

added_engine_file = open("added_from_engine.txt", "w")
added_engine_file.write(str(added_from_engine))
added_dev_file = open("added_from_dev.txt", "w")
added_dev_file.write(str(added_from_dev))
differing_file = open("differing_files.txt", 'w')
differing_file.write(str(differing_files))

print("All done!")
