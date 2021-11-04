import os
from random import shuffle

def getAllFiles(dirName):
    
    #Create a list to store all files
    allFiles = []
    #Get contents of the root directory
    currentDirFiles = os.listdir(dirName)

    #Iterate over all entries
    for file in currentDirFiles:
        #Create full path
        filePATH = os.path.join(dirName, file)
        #Check if directory
        if os.path.isdir(filePATH):
            allFiles += getAllFiles(filePATH)
        else: allFiles.append(filePATH)
    
    return allFiles

print('Where are the movies? ')
PATH = input()
files = getAllFiles(PATH)
shuffle(files)

for file in files:
    os.startfile(file)
    input("Press Enter to continue...")


