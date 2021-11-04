#! /usr/bin/env python3
from appscript import app, mactypes
import time, os, re

for filename in os.listdir('/Library/Desktop Pictures'):
  image = re.compile(r'.jpg')
  mo = image.search(filename)
  if mo != None:
    app('Finder').desktop_picture.set(mactypes.File('/Library/Desktop Pictures/' + filename))
    time.sleep(3)
