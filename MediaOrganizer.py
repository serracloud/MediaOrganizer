#! usr/bin/env

import os, sys, glob, platform, time, shutil
from sys import argv


#TASKS:
# 1. Sort undated files
# 2. Help Script work on Windows
# 3. Comment your functions/code
# 4. Clean Up


def pullDate(path):

    months = {1: ['January', 'Jan'], 2:['February', 'Feb'], 3:['March', 'Mar'], 4:['April', 'Apr'], 5:['May'], 6:['June', 'Jun'], 7:['July', 'Jul'], 8:['August', 'Aug'], 9:['September', 'Sep'], 10:['October', 'Oct'], 11:['November', 'Nov'], 12:['December', 'Dec']}

    if platform.system() == 'Windows':
        fullDate = time.ctime(os.path.getctime(path).split(' '))
        month = ''
        year = ''
        for num, name in months.items():
            for item in fullDate:
                if item in name:
                    month = item.capitalize()
                else:
                    continue
        for item in fullDate:
            if '20' in item and len(item) == 4:
                year = item  
        monthYear = ((month, year))
        return monthYear
    else:
        stat = os.stat(path)
        try:
            fullDate = time.ctime(stat.st_birthtime).split(' ')
            month = ''
            year = ''
            for num, name in months.items():
                for item in fullDate:
                    if item in name:
                        month = item.capitalize()
                    else:
                        continue

            for item in fullDate:
                if '20' in item and len(item) == 4:
                    year = item
                
                
            monthYear = ((month, year))
            return monthYear
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            fullDate = time.ctime(stat.st_mtime).split(' ')
            month = ''
            year = ''
            for num, name in months.items():
                for item in fullDate:
                    if item in name:
                        month = item.capitalize()
                    else:
                        continue
            for item in fullDate:
                if '20' in item and len(item) == 4:
                    year = item                                
            monthYear = ((month, year))
            return monthYear
            
            
            
def createFolder(homepath, month, year):
    """Adds Flexibility: if homepath does not have a slash at the end, the function adds it for you. Then it checks to see if a month/year path exists. If so, it just returns the path. If not, it creates the path, then returns the path. """
    if homepath.endswith('/'):
        newDir = homepath + month + year
        if not os.path.exists(newDir):
            os.makedirs(newDir)
            return newDir
        elif os.path.exists(newDir):
            return newDir
    elif homepath.endswith('/') is False:
        newDir = homepath+ '/' + month + year
        if not os.path.exists(newDir):
            os.makedirs(newDir)
            return newDir
        elif os.path.exists(newDir):
            return newDir



def moveFile(source, dest):
    """shutil.move with a try/except in case file has issues opening."""
    try:
        shutil.move(source, dest) 
    except IOError as e:
        print ("Unable to move file. %s" %(e))
    
    
def getFiles(filepath, fextn):
    filelist = []
    if os.path.exists(filepath):
        filelist.append(glob.glob(filepath + '*.'+fextn.lower(), recursive = True))
        filelist.append(glob.glob(filepath + '*.'+fextn.upper(), recursive = True))
        flatlist = [item for sublist in filelist for item in sublist]
        return flatlist
    else:
        return False
        
        
        
        
        
        
if __name__ == '__main__':
    
    
#    if argv < 3:
#        print("Enter the top level directory AND the file extension that you would like #to sort (i.e. MediaOrganizer.py /home/Desktop/Pictures jpg")
#        sys.exit()
        
    thisscript, pathname, filetype = argv
    
    if pathname is None:
        print ("Enter the top-level path of the directory you want to sort.")
        sys.exit()
    elif os.path.exists(pathname) is False:
        print ("Enter the top-level path of the directory you want to sort (i.e. '/root/Pictures/).")
        sys.exit()
    elif not filetype:
        print ("Enter the file extension you would like to sort (i.e.: jpg, mp4, etc.).")
        sys.exit()
        
    print ("Check below entries for accuracy.\n")
    print ("Your Path is: \t\t", pathname, type(pathname))
    print ("Your filetype is: \t", filetype, type(filetype))
    allFiles = getFiles(pathname, filetype)
    print("List of all Files Retrieved: ", allFiles)
    
    if allFiles is False:
        print("Could not retrieve your files. Check your pathname and/or file extension and rerun the program.")
        sys.exit()
    else:

        for file in allFiles:
            print("Working on file", file)
            mo, yr = pullDate(file)
            print("Month file was last modified: \t", mo)
            print("Year file was last modified: \t", yr)           
            newFolder = createFolder(pathname, mo, yr)
            print("new folder var is :\t", newFolder)
            moveFile(file, newFolder)
            print("File %s MOVED to %s." % (file, newFolder))

    
