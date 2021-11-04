import re, os, shutil

# STEP 1: Enter the PATH of the file directory
SOURCE = "/Volumes/Media/Movies"

def isFormatted(file, regex):
    format = re.compile(regex)
    return format.search(file)

print()
index = 1
for file in os.listdir( SOURCE ) :
    i = str(index).zfill(4)
    oldName = file
    oldPath = os.path.join(SOURCE, oldName)
    newName = ""
    newPath = ""

    correctFormat = r'(.*)\s(\(\d{4}\))\.\w{3}'
    incorrectFormat = r'(.*\s\(\d{4}\)).*(\.\w{3})'
    correctDirFormat = r'(.*)\s(\(\d{4}\))$'
    incorrectDirFormat = r'(.*)\s(\(\d{4}\)).*'
    titleFormat = r'(.*\s\(\d{4}\)).*'
    videoFormat = r'.(mp4|mov|avi|MP4|MOV|AVI|m4v|mkv)'
  
    if os.path.isfile(oldPath) and oldName != '.DS_Store':
        # If it's a file, make sure it's formatterd
        if not isFormatted(oldName, correctFormat): 
            print(f'{i}: FILE NOT FORMATTED: {oldName}')
            isAlmostFormatted = isFormatted(file, incorrectFormat)
            if isAlmostFormatted: newName = f'{isAlmostFormatted.group(1)}{isAlmostFormatted.group(2)}'
            else:
                newName = input('{i}: Cannot determine format. Enter new file name: ')
                while not isFormatted(newName, correctFormat): 
                    print('{i}: New name is not in proper format.  Try again.')
                    newName = input('{i}:: Enter new file name: ')
            newPath = os.path.join(SOURCE, newName)
            print(f'{i}: FORMATTING {oldPath} ==> {newPath}')
            os.rename(oldPath, newPath)              
        # Then create a folder with the same name 
        name = newName if newName else oldName
        title = isFormatted(name, titleFormat)
        newDir = os.path.join(SOURCE, title.group(1))              
        if not os.path.isdir(newDir): 
            print(f'{i}: Creating new directory: {newDir}') 
            os.mkdir(newDir)
        # Move file into the folder
        if os.path.isfile(newPath): 
            print(f'{i}: Moving {newPath} ==> {os.path.join(newDir, newName)}')
            shutil.move(newPath, os.path.join(newDir, newName))
        else: 
            print(f'{i}: Moving {oldPath} ==> {os.path.join(newDir, oldName)}')
            shutil.move(oldPath, os.path.join(newDir, oldName))

    elif os.path.isdir(oldPath):
        if not isFormatted(oldName, correctDirFormat): 
            print(f'{i}: FOLDER NOT FORMATTED: {oldName}')
            isAlmostFormatted = isFormatted(file, incorrectDirFormat)
            if isAlmostFormatted: newName = f'{isAlmostFormatted.group(1)} {isAlmostFormatted.group(2)}'
            else:
                newName = input('{i}: Enter new folder name: ')
                while not isFormatted(newName, correctDirFormat): 
                    print('{i}: New name is not in the proper format.  Try again.')
                    newName = input('{i}: Enter new folder name: ')
            newPath = os.path.join(SOURCE, newName)
            print(f'{i}: FORMATTING {oldPath} ==> {newPath}')
            # TODO Make sure not already exists
            os.rename(oldPath, newPath) 
            
        #check files    
        movieDir = newPath if newPath else oldPath
        for file in os.listdir(movieDir):
            movie = isFormatted(file, videoFormat)
            if movie != None: 
                newFile = f'{newName}.{movie.group(1)}'
                if not isFormatted(file, correctFormat): 
                    print(f'{i}: NOT FORMATTED: {file}')
                    print(f'{i}: FORMATTING {movieDir}/{file} ==> {os.path.join(movieDir, newFile)}')
                    os.rename(os.path.join(movieDir, file), os.path.join(movieDir, newFile))            

    print(f'{i}: FORMATTED {newName if newName else oldName}')
    print()
    index += 1
