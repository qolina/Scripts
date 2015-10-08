# convert tweebank format to conll format.
# 14 fields to 10 fields (ignore last four fields)
# input: file tweebank stype file;
# output: file conll format file

import sys

def tweebank2conll(filename):
    infile = file(filename)
    for lineStr in infile:
        lineStr = lineStr[:-1]
        arr = lineStr.split("\t")

        # selected twitter-specific tagged word
#        if len(arr) > 1:
#            if arr[13]=="1": 
#                if arr[3] in ["@", "#", "U", "E", "~", "G"]:
#                    print lineStr

        if len(arr) == 14:
            print "\t".join(arr[:-4])
        else:
            print lineStr
    infile.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python tweebank2conll.py tweebankStyleFile (> tweebankStyleFile.conll)"
        sys.exit(0)
    tweebank2conll(sys.argv[1])
