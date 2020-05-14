#!/usr/bin/env python3

# Generate clangdb compilation database from a list of complie options

import os, sys, io, glob, json 

cdb = [] 

for f in glob.iglob('**/compile_options.txt', recursive=True):
    print("--- Reading " + f + " ---")
    with open(f, "r") as copt:
        lines = copt.readlines()

        # Add each line, one by one
        for line in lines:
            # Line should be split by token, but this is probably bad because spaces will break it!
            tokens = line.split(" ")
            entry = {}
            _path = tokens[len(tokens)-1]
            entry["directory"] = os.path.dirname(_path)
            entry["command"] = tokens
            entry["file"] = _path
            cdb.append(entry)


with open("compile_commands.json", "w") as fs:
    print("Writing compile_commands.json")
    json.dump(cdb, fs, indent=4)


            
