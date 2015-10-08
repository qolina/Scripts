# convert dependency formated penn to new POS (tag set used in Tweebank and CMU-ark Twitter specific tag set)
# input: file penn treebank dependency stype file;
# output: file replaced POS tag file

import sys
from posTag2TwiTag import *
from hashOperation import *


# tag is Penn pos tag
def isSpecialWord(word, tag):
    if word.startswith("'"):
        if tag == "POS":
            return True
        elif tag.startswith("V") or tag == "MD":
            return True
    return False


# words tagged to 
# S nominal+possessive (others + POS)
# Z proper noun + possesive  (NNP|NNPS + POS)
# L nominal + verbal  (others + V*|MD)
# M proper noun + verbal  (NNP|NNPS + V*|MD)
# Y X + verbal  (X: EX|PDT)
def pennTag2SpecialTweTag(word, tag, tag_preWord):
    if word.startswith("'"):
        if tag == "POS":
            if tag_preWord.startswith("NNP"):
                return "Z"
            else:
                return "S"
        elif tag.startswith("V") or tag == "MD":
            if tag_preWord in ["EX", "PDT"]:
                return "Y"
            elif tag_preWord.startswith("NNP"):
                return "M"
            else:
                return "L"
    return None


#conll format: idx, word, _, pos, pos, _, head, _, _, _
def penn_changePos(filename):
    unmappedTag = {}
    specialWordHash = {}

    infile = file(filename)
    
    newLines = []
    for lineStr in infile:
        lineStr = lineStr[:-1]
        arr = lineStr.split("\t")
        if len(arr) > 1:
            oldTag = arr[3]
            newTag = pos2TwiTag(oldTag)

            # spcial tag
            word = arr[1]
            if isSpecialWord(arr[1], oldTag):
                preWordArr = newLines[-1].split("\t")
                if len(preWordArr) > 1:
                    pennTag_preWord = preWordArr[4]
                    newTag = pennTag2SpecialTweTag(arr[1], oldTag, pennTag_preWord)
                specialWordHash = cumulativeInsert(specialWordHash, arr[1]+"/"+newTag+"/"+oldTag, 1)
                #print [arr[1], oldTag, pennTag_preWord, newTag]

            if newTag is None:
                unmappedTag[oldTag] = 1
            else:
                arr[3] = newTag
                arr[4] = oldTag
                newLines.append("\t".join(arr))

        else:
            newLines.append(lineStr)
    infile.close()

    # output specialWord Distribution 2 terminal
#    print sorted(specialWordHash.items(), key = lambda a:a[1], reverse = True)
#    specialWordHash_ratio = count2Ratio(specialWordHash)
#    print sorted(specialWordHash_ratio.items(), key = lambda a:a[1], reverse = True)
#    for item in sorted(specialWordHash_ratio.items(), key = lambda a:a[1], reverse = True):
#        print item[0], "\t", specialWordHash[item[0]], "\t",  item[1]

    # print to terminal
    if len(unmappedTag.keys()) == 0:
        print "\n".join(newLines)
    else:
        print "Error. UnmappedTags", unmappedTag.keys()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: (change pennPOS to CMU-ark Twitter-specific POS tags) python penn_changePos.py pennDepFile (> penn.conll)"
        sys.exit(0)
    penn_changePos(sys.argv[1])


