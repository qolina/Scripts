import sys


def split_file(inFilename, suffix):
    if suffix == "01":
        suffixArr = [str(num).zfill(2) for num in range(1, 100)]

    print suffixArr

    inFile = file(inFilename)
    contents = inFile.readlines()
    inFile.close()

    sepContent = "".join(contents).split("*****\n")
    sepContent = [item for item in sepContent if len(item) > 1]

    print "Total parts: ", len(sepContent)
    for i in range(len(sepContent)):
        outFile = file(inFilename+suffixArr[i], "w")
        outFile.write(sepContent[i])
        outFile.close()


def getArg(args, flag):
    arg = None
    if flag in args:
        arg = args[args.index(flag)+1]
    return arg

def parseArgs(args):
    arg1 = getArg(args, "-in")
    if arg1 is None:
        sys.exit(0)
        
    arg2 = getArg(args, "-suf")

    return arg1, arg2




#######################################################
## main
if __name__ == "__main__":

    print "Usage: python split_file_by_content.py -in infilename -suf suffix (01, 1, a, aa)"

    [inFilename, suffix] = parseArgs(sys.argv)

    split_file(inFilename, suffix)
