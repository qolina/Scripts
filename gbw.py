import os
import sys
import cPickle
from duplication_rm import uniq
import time

print "Usage python gbw.py gbwFilename, tolabelgramFilename"

nolabelGram = uniq(sys.argv[2])

dirPath = sys.argv[1]

wordsHash = {}
gramEntropyHash = {}
gramsHash = {}

for filename in sorted(os.listdir(dirPath)):
    if filename.endswith(".tar"): continue
    print "## Reading", filename
    content = file(dirPath + filename, "r").readlines()

    words = []
    lineIdx = 0

    while lineIdx < len(content):
        line = content[lineIdx]
        if line.startswith("WORDS"):
            words = line.strip("WORDS:").strip().split()
            wordids = content[lineIdx+1].strip("WORD IDS:").strip().split()
            wordsHash.update(dict(zip(wordids, words)))
        wordnum = len(words)
        #print "#####################################"
        #print "---total line###", content[lineIdx+2+2*(wordnum-1)]
        for li in range(lineIdx+2, lineIdx+2+2*(wordnum-1)):
            wordline = content[li].strip()
            if wordline[0] == "|": continue
            #print wordline
            inforArr = wordline.split()
            #print inforArr
            word, wordid = inforArr[:2]
            wordseqId = (li-lineIdx-2)/2%(wordnum-1) + 1
            grams = inforArr[3:-2]
            #print word, wordid, wordseqId, grams
            for gramlen in range(1, len(grams)+1):
                entropy = grams[-gramlen]
                gram = "_".join(words[wordseqId-gramlen+1:wordseqId+1]).lower()
                #print gram, entropy
                gramsHash[gram] = 1

                if gram not in gramEntropyHash:
                    if gram in nolabelGram:
                        gramEntropyHash[gram] = entropy
                #else:
                #    print "##Existed", gram, entropy, gramEntropyHash[gram]

        lineIdx += 2+2*(wordnum-1)+1
        #break

print "## Summary #gramwithEntropy, #words", len(gramEntropyHash), len(wordsHash), time.asctime(), len(gramsHash)
outFile = open("/home/yanxia/SED/ni_data/word/grams/entropyGrams", "w") #+os.path.basename(filename)
cPickle.dump(gramEntropyHash, outFile)
print "# Writen to", outFile.name
