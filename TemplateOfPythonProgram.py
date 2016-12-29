## function
## [to be filled]

import sys
import os
import re
import time


##############
def getArg(args, flag):
    arg = None
    if flag in args:
        arg = args[args.index(flag)+1]
    return arg

# arguments received from arguments
def parseArgs(args):
    arg1 = getArg(args, "-in")
    if arg1 is None: # nessensary argument
        print "Usage: python example.py -in inputFilename"
        sys.exit(0)
    return arg1


####################################################
if __name__ == "__main__":
    conll_filename = parseArgs(sys.argv)

    print "Program starts at ", time.asctime()

    print "Program ends at ", time.asctime()
