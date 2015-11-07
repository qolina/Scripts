import sys
import time
import cPickle
import os

def extractHeadlines_fromDailyNews(newsDirPath):
    headlineHash = {} # day:headlineList [headline1, headline2]

    dirList = os.listdir(newsDirPath)
    for dirPath in sorted(dirList):
        if not os.path.isdir(newsDirPath + "/" + dirPath):
            continue
        day = dirPath
        headlineList = extractHeadlines_fromDayDir(newsDirPath + "/" + dirPath)
        headlineHash[day] = headlineList
    return headlineHash


def extractHeadlines_fromDayDir(dirPath):
    headlineList = []
    fileList = os.listdir(dirPath)
    for item in sorted(fileList):
        if not os.path.isfile(dirPath + "/" + item):
            continue
        headline = extractHeadline_fromFile(dirPath + "/" + item)
        headlineList.append(headline)
    return headlineList


def extractHeadline_fromFile(filePath):
    newsFile = file(filePath)
    contentArr = newsFile.readlines()
    contentArr = [line[:-1] for line in contentArr]
    newsFile.close()

    headline = contentArr[0].strip("-- ")
#    authors = contentArr[1].strip("-- ")
#    published_time = contentArr[2].strip("-- ")
#    url = contentArr[3].strip("-- ")
#    text = "\n".join(contentArr[4:])

    return headline

def write2File(headlineHash, outFilename):
    outFile = file(outFilename, "w")
    cPickle.dump(headlineHash, outFile)
    outFile.close()
    print "** Content has been stored into", outFilename


def getArg(args, flag):
    arg = None
    if flag in args:
        arg = args[args.index(flag)+1]
    return arg

def parseArgs(args):
    arg1 = getArg(args, "-dir")
    arg2 = getArg(args, "-out")

    if (arg1 is None) or (arg2 is None):
        print "Usage: python extractHeadlinesForStockNews.py -dir newsDirPath -out output_headlines_filename"
        sys.exit(0)
    return arg1, arg2

#######################################################
## main
if __name__ == "__main__":

    print "Program starts at time:" + str(time.asctime())
    [newsDirPath, outFilename] = parseArgs(sys.argv)

    headlineHash = extractHeadlines_fromDailyNews(newsDirPath)
    print "**", len(headlineHash), " days of news are obtained. #totalNews:", sum([len(list) for list in headlineHash.values()])
    write2File(headlineHash, outFilename)

    print "Program ends at time:" + str(time.asctime())

