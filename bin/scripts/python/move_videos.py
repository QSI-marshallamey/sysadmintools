#! /usr/bin/env python3

########################################################################
# Author: Marshall Amey
# Date: Nov 10, 2019
# This script moves all uploaded photos to the 'Photos' directory from 'Automatic Uploads'
# The default directory is in pCloud, but you can specify a different source folder as an argument
# iPhone photos are named with a TIMESTAMP in the format 'YYYY-MM-DD hh-mm-ss.jpeg'. 
# This will not work for photos with different naming convention
########################################################################

import re, os, shutil, datetime

def move_videos():

    SOURCE = "/Users/marshallamey/pCloud Drive/Media/Photos"
    DESTINATION = "/Users/marshallamey/pCloud Drive/Media/Videos"
    TIMESTAMP = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print( f"{TIMESTAMP}:: Checking {SOURCE} for videos..." )

    # Find all uploaded iPhone photos and videos
    video = re.compile(r'.(mp4|mov|avi|MP4|MOV|AVI|m4v|mkv)')
    for root, dir, files in os.walk( SOURCE ) :  
        

        for filename in files:
            # Check if file is a video
            result = video.search(os.path.join(root,filename))
            if result == None: continue

            # Rename the video
            sourceFile = os.path.join(root, filename)
            destFile = os.path.join(DESTINATION, filename)

            # Move file into destination
            print( f"{TIMESTAMP}:: {sourceFile} ==> {destFile}" )
            shutil.move(sourceFile, destFile)

if __name__ == "__main__": move_videos()