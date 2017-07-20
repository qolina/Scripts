import sys
import time
import cPickle
from google_ngram_downloader import * #readline_google_store
from google_ngram_downloader.util import *
from duplication_rm import uniq

def match_from_files(fileIter, tolabelGram):
    countArr = []
    numArr = []
    labeledGramHash = {}
    while 1:
        try:
            grams_count_len = 0
            grams_num = 0

            fname, url, records = next(fileIter)
            print "## Reading", fname, time.asctime() #, url
            while 1:
            #for i in range(1000):
                try:
                    record = next(records)
                    gram, year, match_count, volume_count = record
                    #if year < "2000": continue
                    match_count = int(match_count)
                    if match_count < 50: continue
                    grams_count_len += match_count
                    grams_num += 1
                    gram = gram.replace(" ", "_")
                    if gram in tolabelGram:
                        tolabelGram[gram] += match_count
                    #print gram, year, match_count
                except StopIteration: break
            labeledGram = dict([item for item in tolabelGram.items() if item[1] > 0])
            print grams_num, grams_count_len, len(labeledGram)
            countArr.append(grams_count_len)
            numArr.append(grams_num)
            labeledGramHash.update(labeledGram)
        except StopIteration: break
    return labeledGramHash, countArr, numArr


glen = int(sys.argv[2])
nolabelGram = uniq(sys.argv[1])
allGrams = []

#for glen in range(1, 6):
if glen in range(1, 6):
    print "gram_length, grams_number", glen,
    grams = sorted([(gram, glen) for gram in nolabelGram if len(gram.split("_")) == glen])
    print len(grams)
    grams_numArr = []
    grams_countArr = []
    gramsCountHash = {}
    glen_indices = [item for item in get_indices(glen)]
    #print glen_indices
    regularIndic = [item for item in glen_indices if len(item) <= 2]
    #print regularIndic
    for indic in regularIndic:
        grams_indic = dict([(gram, 0) for gram, gl in grams if gram.startswith(indic)])
        print indic, len(grams_indic)

        fileIter = readline_google_store(ngram_len=glen, indices=[indic])
        labeledGram, countArr, numArr = match_from_files(fileIter, grams_indic)
        gramsCountHash.update(labeledGram)
        grams_numArr.extend(numArr)
        grams_countArr.extend(countArr)
        break
    other_indic = [item for item in glen_indices if len(item) > 2]
    print other_indic, 
    grams_indic = dict([(gram, 0) for gram, gl in grams if gram[0] not in regularIndic and gram[:2] not in regularIndic])
    print len(grams_indic)
    fileIter = readline_google_store(ngram_len=glen, indices=other_indic)
    labeledGram, countArr, numArr = match_from_files(fileIter, grams_indic)
    gramsCountHash.update(labeledGram)
    grams_numArr.extend(numArr)
    grams_countArr.extend(countArr)

    outFile = open("/home/yanxia/SED/ni_data/word/grams/countGrams"+str(glen), "w")
    cPickle.dump(gramsCountHash, outFile)
    cPickle.dump(grams_numArr, outFile)
    cPickle.dump(grams_countArr, outFile)
    print "##", len(gramsCountHash), outFile.name

print "## ends", time.asctime()
