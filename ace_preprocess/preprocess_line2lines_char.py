from collections import Counter

def convert_word(word, wordTag):
    wordLen = len(word)
    if wordLen == 1:
        return [(word, "B-"+wordTag if wordTag!='O' else wordTag)]
    # only keep first two chars if wordLen>=2
    if wordTag == "O":
        charTagArr = ["O"] * wordLen
    else:
        charTagArr = ["B-" + wordTag]
        if wordLen > 1: charTagArr.extend(["I-" + wordTag]*(wordLen-1))
    return list(zip(word, charTagArr))


def convert(inFilename, outFilename, typeDict):
    seqLens = []
    outfile = open(outFilename, "w")
    contentArr = open(inFilename, "r").readlines()
    for lineId, line in enumerate(contentArr):
        sentStr, tagStr = line.rstrip("\n").split("\t")[:2]
        charSeqTagOfSent = []
        wordArr = sentStr.split(" ")
        tagArr = [typeDict[wordTag] if wordTag != "O" else wordTag for wordTag in tagStr.split(" ")]
        for word, wordTag in zip(wordArr, tagArr):
            charsTagsSeq = convert_word(word, wordTag)
            charSeqTagOfSent.extend(charsTagsSeq)

        outfile.write("\n".join([item[0]+" "+item[1] for item in charSeqTagOfSent]))
        if lineId < len(contentArr)-1: outfile.write("\n\n")
        seqLens.append(len(charSeqTagOfSent))

    outfile.close()
    print(min(seqLens), max(seqLens), Counter(seqLens).most_common())

if __name__ == "__main__":

    dirPrefix = "./char/"
    arr = open("./ACE_event_types.txt").readlines()
    arr = [line.rstrip("\n").split("\t") for line in arr]
    typeDict = dict([(item[0], item[2]) for item in arr])
    bio_types = ["B-"+item[2] for item in arr]
    bio_types.extend(["I-"+item[2] for item in arr])
    label_out_file = open(dirPrefix+"labels.txt", "w")
    label_out_file.write("\n".join(sorted(bio_types)))
    label_out_file.close()

    convert("./cn_trig_ner_arg.train.txt", dirPrefix+"train.txt", typeDict)
    convert("./cn_trig_ner_arg.dev.txt", dirPrefix+"dev.txt", typeDict)
    convert("./cn_trig_ner_arg.test.txt", dirPrefix+"test.txt", typeDict)
