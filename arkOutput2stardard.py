# convert cmu-ark tagger (with model.ritter pennTagset) pos-tagged output file into normal format
# cmu-ark format 1: word word[\t]tag tag[\t]confidence score[\t]meaningful word sequence?
# cmu-ark format 2:
#                    word[\t]tag[\t]score
#                    word[\t]tag[\t]score
# standard: word/tag word/tag ...

import sys


def arkOut2stand(arkFilename):
    arkFile = file(arkFilename)
    content = arkFile.readlines()
    for lineStr in content:
        partsArr = lineStr.split("\t")

        wordsStr = partsArr[0]
        tagsStr = partsArr[1]

        words = wordsStr.strip().split(" ")
        tags = tagsStr.strip().split(" ")
        
#        print words
#        print tags

        if len(words) != len(tags):
            print "Error!"
            break

        taggedWords = [words[i]+"/"+tags[i] for i in range(len(words))]
        print " ".join(taggedWords)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: (change CMU-ark pennTag output file into standard pennTag output) python arkOutput2Standard.py data.arkTagged_pennTag (> data.tagged.standard)"
        sys.exit(0)
    arkOut2stand(sys.argv[1])
#    arkOut_conll2stand(sys.argv[1])
