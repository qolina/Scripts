
import os
import sys
# pos-tagging, np chunking, ner tagging for segmented chinese finance news.

from nltk.tag.stanford import StanfordPOSTagger
from nltk.tag import StanfordNERTagger

if __name__ == "__main__":
    pos_tagger = StanfordPOSTagger("chinese-distsim.tagger")
    ner_tagger = StanfordNERTagger("chinese.misc.distsim.crf.ser.gz")
    #ner_tagger = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
    #ner_tagger.tag("i like apple .".split())

    print sys.argv
    dirPath = sys.argv[1]

    fileList = os.listdir(dirPath)
    for segfile in sorted(fileList):
        contents = open(dirPath+segfile, "r").readlines()
        for line in contents:
            print line
            words = line.split()
            words_pos = pos_tagger.tag(words)
            for item in words_pos:
                print item[1]
            words_ner = ner_tagger.tag(words)
            for item in words_ner:
                print item[0], item[1]

        break

