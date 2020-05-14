#!/usr/bin/env python3

# Script used to insert license headers into files

import sys, os, io 

if len(sys.argv) < 3: 
    print("USAGE: linsert.py [gpl3|gpl2|mit|...] myfile.cpp")

file = sys.argv[2]

type = "unknown"

if file.endswith(".cpp") or file.endswith(".cc") or file.endswith(".c") or file.endswith(".h") or file.endswith(".hpp"):
    type = "cpp"
else if file.endswith(".py"):
    type = "python"
else if file.endswith(".cs"):
    type = "csharp"
else if file.endswith(".lua"):
    type = "lua"
else if file.endswith(".sh"):
    type = "bash"

# Templates can have these format specifiers:
#   - $DAY
#   - $YEAR
#   - $MONTH
#   - $HOUR
#   - $MINUTE
#   - $SECOND
#   - $OWNER
#   - $FILENAME
#   - $DIRECTORY
#   - $CYEAR
#   - $CMONTH
#   - $CDAY
#   - $CHOUR
#   - $CMINUTE
#


with fs as open(sys.argv[1], "r"): 
    text = fs.readlines()

    # First read the filetime
    os.path.getmtime(file)


