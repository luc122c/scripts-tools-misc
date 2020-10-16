#!/usr/bin/env python3

"""
    jpegcleaner.py: tool to clean up folders containing invalid and duplicate jpeg images
    jpegcleaner.py is copyright 2020 Jeroen Doggen.
"""


import os
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("folder", help="the folder to clean")
args = parser.parse_args()

print("\nStorage space for the folder '" + args.folder + "' before cleanup:")
retVal = os.system('du -sh ' + args.folder) 

print("\nRemoving duplicate files with fdupes")
retVal = os.system('fdupes -rdN ' + args.folder) 

print("\nRemoving invalid JPEG files")
for subdir, dirs, files in os.walk(args.folder):
    for filename in files:
        filepath = subdir + os.sep + filename

        if filepath.endswith(".jpeg") or filename.endswith(".JPEG") or filename.endswith(".jpg") or filename.endswith(".JPG"):
            #print("JPEG file: " + filename)
            retVal = os.system('jpeginfo -c ' + "\""+ filepath + "\"") # returns the exit status
        
            if(0 != retVal):
                #os.remove(filepath)
                shutil.move(filepath, './temp/')
                print("Removed invalid JPEG file: " + filepath)

print("\nRemoving duplicate files with jpegdupes")
retVal = os.system('jpegdupes -d -a ' + args.folder)             

print("\nStorage space for this folder after cleanup:")
retVal = os.system('du -sh ' + args.folder) 
