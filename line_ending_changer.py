from file_functions import *

location = "oldUE"
line_ending_sensitive = {".cpp", ".h", ".xml", ".cs", ".usf", ".ush", ".txt", ".ini", ".sh", ".m", ".vxproj", ".c", ".mm", ".html", ".cmake", ".inl", ".config", ".csproj", ".uplugin", ".template", ".java", ".py"}


def convert_line_ending(file):
    extension = os.path.splitext(file)[1]
    if (extension in line_ending_sensitive):
        inp = open(file, 'rb')
        txt = inp.read()
        txt = txt.replace('\r'.encode(), "".encode())
        txt = txt.replace('\n'.encode(), '\r\n'.encode())
        inp.close()
        try:
            out = open(file, 'wb')
            out.write(txt)
            out.close()
        except:
            print("unable to change lines of file: " + file)

execute_for_all_files(location, convert_line_ending)
