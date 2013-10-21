import os.system
import time
from PathUtils import PathUtils

os.system(command)

def runnable():
    #dectect any file in directory
    PathUtils().get_list_filename("D:\\z\\")

    time.sleep(5) #waiting for 5s
    runnable()

    print "ok"
