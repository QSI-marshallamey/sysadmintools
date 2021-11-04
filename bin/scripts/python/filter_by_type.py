#! python3
# fileFilter.py - Organizes files in Downloads by placing them in designated folders

import shutil, os, re

PATH = '/Users/marshallamey/Downloads/'

# Create regex patterns to match file type
excel = re.compile(r'.(xls|xlsx)')
word = re.compile(r'.(doc|docx)')
image = re.compile(r'.(jpeg|jpg|png|gif)')
video = re.compile(r'.(mp4|mov|avi|MP4|MOV|AVI|m4v|mkv)')
music = re.compile(r'.(mp3|wav|aiff)')
pdf = re.compile(r'.pdf')
cpp = re.compile(r'.cpp')
illustrator = re.compile(r'.ai')
powerpoint = re.compile(r'.(ppt|pptx)')
py = re.compile(r'.py')

# Loop through files in PATH
for filename in os.listdir(PATH):

    ## Move Excel files
    mo = excel.search(filename)
    
    if mo != None: 
        shutil.move(PATH + filename, PATH + 'Spreadsheets/' + filename)
        continue

    ## Move Word files
    mo = word.search(filename)
    
    if mo != None: 
        shutil.move(PATH + filename, PATH + 'Docs/' + filename)
        continue

    ## Move image files
    mo = image.search(filename)
    
    if mo != None: 
        shutil.move(PATH + filename, PATH + 'Pictures/' + filename)
        continue
    
    ## Move cpp files
    mo = cpp.search(filename)
    
    if mo != None: 
        shutil.move(PATH + filename, PATH + 'CPlusPlus/' + filename)
        continue

    ## Move PDF files
    mo = pdf.search(filename)
    
    if mo != None: 
        shutil.move(PATH + filename, PATH + 'PDFs/' + filename)
        continue

    ## Move python files
    mo = py.search(filename)
    
    if mo != None: 
        shutil.move(PATH + filename, PATH + 'Python/' + filename)
        continue

    ## Move Illustrator files
    mo = illustrator.search(filename)
    
    if mo != None: 
        shutil.move(PATH + filename, PATH + 'Illustrator/' + filename)
        continue

    ## Move Powerpoint files
    mo = powerpoint.search(filename)
    
    if mo != None: 
        shutil.move(PATH + filename, PATH + 'Powerpoints/' + filename)
        continue

    ## Move video files
    mo = video.search(filename)
    
    if mo != None: 
        shutil.move(PATH + filename, PATH + 'Videos/' + filename)
        continue

    ## Move music files
    mo = music.search(filename)
    
    if mo != None: 
        shutil.move(PATH + filename, PATH + 'Music/' + filename)
        continue


