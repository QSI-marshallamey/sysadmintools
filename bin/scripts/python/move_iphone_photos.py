#! /usr/bin/env/python3

########################################################################
# Author: Marshall Amey
# Date: Nov 10, 2019
# This script moves all uploaded photos to the 'Photos' directory from 'Automatic Uploads'
# The default directory is in pCloud, but you can specify a different source folder as an argument
# iPhone photos are named with a timestamp in the format 'YYYY-MM-DD hh-mm-ss.jpeg'. 
# This will not work for photos with different naming convention
########################################################################

import re, os, shutil

def move_iphone_photos(source = "/Users/marshallamey/pCloud Drive/Automatic Upload/Marshall’s iPhone"):

    SOURCE = source
    DESTINATION = "/Users/marshallamey/pCloud Drive/Media/Photos"

    # Find all uploaded iPhone photos and videos
    photoRegex = re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d)')
    for photo in os.listdir( SOURCE ) :

        # Get date from filename
        date = photoRegex.search(photo)
        if date == None: continue
        year = date.group(1)
        month = date.group(2)
        day = date.group(3)

        # Create year directory if not exists
        yearFolder = os.path.join(DESTINATION, year)
        if not os.path.isdir( yearFolder ):
            os.makedirs( os.path.join(DESTINATION, year) )
            for i in range(12): os.makedirs( os.path.join( DESTINATION, year, f"{i+1:02d}" ) )

        # Rename the file
        sourceFile = os.path.join(SOURCE, photo)
        destFile = os.path.join(DESTINATION, year, month, photo)

        # Move file into destination
        print( f"Renaming {sourceFile} to {destFile}" )
        shutil.move(sourceFile, destFile)

if __name__ == "__main__": move_iphone_photos()