import sys
import os
import re
import time

import jieba
import thulac
from snownlp import SnowNLP
import pkuseg

MODE = "pku" # jieba, thulac, snow, pku, han
if MODE == "thulac":
    segmenter = thulac.thulac(seg_only=True)
elif MODE == "pku":
    segmenter = pkuseg.pkuseg()
elif MODE == "han":
    from pyhanlp import HanLP


def convert_word(word, wordTag):
    wordLen = len(word)
    if wordTag == "O":
        charTagArr = ["O"] * wordLen
    else:
        charTagArr = ["B-" + wordTag]
        if wordLen > 1: charTagArr.extend(["I-" + wordTag]*(wordLen-1))
        #print("word, wordTag:", word, wordTag, wordLen, list(zip(word, charTagArr)))
    return list(zip(word, charTagArr))

# words: [word, word, word, ...]
# wordPos: [(char_st, char_ed), (char_st, char_ed), ...]
def resegment(sent):
    # jieba
    if MODE == "jieba":
        words = list(jieba.cut(sent))
    elif MODE == "thulac":
        words = [item[0] for item in segmenter.cut(sent)]
    elif MODE == "snow":
        words = SnowNLP(sent).words
    elif MODE == "pku":
        words = segmenter.cut(sent)
    elif MODE == "han":
        words = [item.word for item in HanLP.segment(sent)]
    #print(sent, words)

    wordPos = []
    search_st = 0
    for word in words:
        st = sent.find(word, search_st)
        ed = st+len(word)-1
        wordPos.append((st, ed))
        #print(word, (st, ed))
    return words, wordPos

# wordTags = [tag, tag, tag]
def align_autoword_char(words, wordPos, charTags):
    wordTags = []
    for word, (st, ed) in zip(words, wordPos):
        tags = charTags[st:ed+1]
        tags_temp1 = [0 if item[1]=="O" else 1 for item in tags]
        if(sum(tags_temp1)==0): wordTags.append("O")
        elif(sum(tags_temp1)<(ed-st+1)): # mismatched, contain trigger, non-trigger
                wordTags.append("O")
                #print("missed: mixed", word, tags)
        else: # all trigger chars
            if(sum([1 if item[1][:2]=="B-" else 0 for item in tags])==1 and tags[0][1][:2]=="B-" and charTags[ed+1][1]!="I-"+tags[0][1][2:]):
                wordTags.append(tags[0][1][2:])
                #print("--correct", word, tags)
            else: # mismatched, contain two triggers
                wordTags.append("O")
                #print("--missed: contain more", word, tags)
    return wordTags

def stat_mismatch(newWords, newWordTags, wordArr, tagArr):
    print("--New", list(zip(newWords, newWordTags)))
    matched, mismatched = 0, 0
    search_st = -1
    for word, wordTag in zip(wordArr, tagArr):
        search_st += 1
        if wordTag != "O":
            if word in newWords and newWordTags[newWords.index(word)]==wordTag:
                matched += 1
                print("--match", word, wordTag, newWordTags[newWords.index(word)])
            else:
                mismatched += 1
                print("--mismatch", word, wordTag)
    newTriggers = [item for item in list(zip(newWords, newWordTags)) if item[1]!="O"]
    if matched != len(newTriggers): print("--Wrong stat", newTriggers)
    return matched, mismatched

def convert(inFilename, outFilename, typeDict):
    outfile = open(outFilename, "w")
    total, matched, missed = 0,0,0
    contentArr = open(inFilename, "r").readlines()
    for lineId, line in enumerate(contentArr):
        sentStr, tagStr = line.rstrip("\n").split("\t")[:2]
        charTagArrOfSent = []
        wordArr = sentStr.split(" ")
        tagArr = [typeDict[wordTag] if wordTag != "O" else wordTag for wordTag in tagStr.split(" ")]
        for word, wordTag in zip(wordArr, tagArr):
            charSeq = convert_word(word, wordTag)
            charTagArrOfSent.extend(charSeq)
        #print("---current charTags: ", charTagArrOfSent)

        autoWords, wordPos = resegment("".join(wordArr))
        wordTags = align_autoword_char(autoWords, wordPos, charTagArrOfSent)
        matched_s, missed_s = stat_mismatch(autoWords, wordTags, wordArr, tagArr)
        matched += matched_s
        missed += missed_s

        #break
        outfile.write(" ".join(autoWords)+"\t"+" ".join(wordTags))
        if lineId < len(contentArr)-1: outfile.write("\n")

    total = matched+missed
    match_ratio = matched*100.0/total
    print(inFilename, " Statistics of mismatching: total", total, "matched", matched, "%.2f"%match_ratio, "mismatched", missed, "%.2f"%(100-match_ratio))
    return matched, missed

if __name__ == "__main__":
    #convert_word("这是1229我", "ABC")
    #convert_word("229ab'我", "ABC")
    #sys.exit(0)

    arr = open("./ACE_event_types.txt").readlines()
    arr = [line.rstrip("\n").split("\t") for line in arr]
    typeDict = dict([(line[0], line[2]) for line in arr])
    matched_1, missed_1 = convert("./cn_trig_ner_arg.train.txt", "cn_trig_autoseg.train.txt", typeDict)
    matched_2, missed_2 = convert("./cn_trig_ner_arg.dev.txt", "cn_trig_autoseg.dev.txt", typeDict)
    matched_3, missed_3 = convert("./cn_trig_ner_arg.test.txt", "cn_trig_autoseg.test.txt", typeDict)

    matched = matched_1 + matched_2 + matched_3
    missed = missed_1 + missed_2 + missed_3
    total = matched+missed
    match_ratio = matched*100.0/total
    print("Statistics of mismatching: total", total, "matched", matched, "%.2f"%match_ratio, "mismatched", missed, "%.2f"%(100-match_ratio))
