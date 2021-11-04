#! /usr/bin/env/python3

####
# This script renames all files in a directory that match an expression
# Change the values in the 3 steps to modify
# Author: Marshall Amey
# Date:   Nov 10, 2019
####

import re, os, shutil

# STEP 1: Enter the PATH of the file directory
SOURCE = "/Volumes/Storage/Personal"

# STEP 2: Enter the expression for filename search
fileRegex = re.compile(r'00(.*)')

# Look for matching files and change the name
for file in os.listdir( SOURCE ) :
    # Get the part of the name you want to keep
    oldName = fileRegex.search(file)
    if oldName == None: continue
    
    # STEP 3: Create the new filename
    newName = oldName.group(1)

    # Rename the file
    oldFile = os.path.join(SOURCE, oldName)
    newFile = os.path.join(SOURCE, newName)
    print( f"Renaming {oldFile} to {newFile}" )
    shutil.move(oldFile, newFile)
