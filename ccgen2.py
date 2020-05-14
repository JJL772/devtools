#!/usr/bin/env python3

# Generate clang db databases from VPC makefiles
import os, sys, json, glob

# Remove the compile commands in the root
try:
    os.remove("compile_commands.json")
except:
    pass

num_read = 0
cdb = []

for _file in glob.iglob("**/*_linux32*.mak", recursive=True):
    includes = []
    files = []
    defines = []
    with open(_file, "r") as fs:
        num_read += 1
        lines = fs.readlines()
        reading_files = False
        print("--> Reading " + _file)
        for line in lines:
            if reading_files:
                if line == "" or line == "\n":
                    reading_files = False
                    continue 
                # Append file & fix it up & append the directory prefix
                files.append(os.path.dirname(_file) + "/" + line.replace("\\", "").rstrip().lstrip())

            else:
                if line.startswith("CPPFILES="):
                    reading_files = True
                    continue

            if line.startswith("DEFINES=") and len(defines) == 0:
                defines += line.replace("DEFINES=", "").split(" ")
            if line.startswith("INCLUDEDIRS +=") and len(includes) == 0:
                includes += line.replace("INCLUDEDIRS +=", "").split(" ")
    # Write the compile commands in the root dir
    for file in files:
        _entry = {}
        _entry["directory"] = os.getcwd() + "/" + os.path.dirname(_file)
        _entry["arguments"] = ['gcc']
        _entry["arguments"] += defines
        # Add prefix to includes
        _entry["arguments"] += (["-I" + x for x in includes])
        #_entry["arguments"].append(includes)
        _entry["file"] = os.getcwd() + "/" + file
        cdb.append(_entry)

with open("compile_commands.json", "w") as fs:
    json.dump(cdb, fs, indent=4)

print("Read " + str(num_read) + " makefiles...")
print("Writing compile_commands.json")
