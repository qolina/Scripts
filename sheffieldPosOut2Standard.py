
import sys

def sheffield2standard(lineStr):
    words = lineStr.split(" ")
    newWords = [word[:word.rfind("_")] + "/" + word[word.rfind("_")+1:]  for word in words]
    return " ".join(newWords)

if __name__ == "__main__":
    filename = sys.argv[1]
    inFile = file(filename)
    while 1:
        lineStr = inFile.readline()
        if not lineStr:
#            print "End of file."
            break
        lineStr = lineStr[:-1]
        print sheffield2standard(lineStr)

