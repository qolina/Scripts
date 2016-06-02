import sys

def getArg(args, flag):
    arg = None
    if flag in args:
        arg = args[args.index(flag)+1]
    return arg

#### 
#example
def parseArgs_eg(args):
    jsonFileName = getArg(args, "-json")
    if jsonFileName is None:
        sys.exit(0)
    outFileName_tweetText = getArg(args, "-textOut")
    outFileName_tweetStruct = getArg(args, "-structOut")
    return jsonFileName, outFileName_tweetText, outFileName_tweetStruct


if __name__ == "main":
    print "Usage: python test.py -json jsonFilename [-textOut textOutput] [-struct structOutput]"

    [jsonFileName, outFileName_tweetText, outFileName_tweetStruct] = parseArgs_eg(sys.argv)
