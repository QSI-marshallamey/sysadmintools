#!/usr/bin/env python3
########################################################################
# Author: Marshall Amey
# Date: Nov 10, 2019
# This script configures a new home computer and installs my favorite software
########################################################################

from sys import platform

def choose_os(): 
    if platform.startswith('linux'): return 'linux-setup.py'      
    elif platform == 'darwin': return 'mac-setup.py'      
    elif platform == 'win32': return 'windows-setup.py'

if __name__ == '__main__': choose_os()