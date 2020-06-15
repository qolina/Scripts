
def convert(inFilename, outFilename, typeDict):
    outfile = open(outFilename, "w")
    contentArr = open(inFilename, "r").readlines()
    for lineId, line in enumerate(contentArr):
        sentStr, tagStr = line.rstrip("\n").split("\t")[:2]
        wordArr = sentStr.split(" ")
        tagArr = [typeDict[wordTag] if wordTag != "O" else wordTag for wordTag in tagStr.split(" ")]
        for word, wordTag in zip(wordArr, tagArr):
            outfile.write(word+" "+wordTag+"\n")
        if lineId < len(contentArr)-1: outfile.write("\n")

    outfile.close()

if __name__ == "__main__":

    arr = open("./ACE_event_types.txt").readlines()
    arr = [line.rstrip("\n").split("\t") for line in arr]
    typeDict = dict([(line[0], "B-"+line[2]) for line in arr])
    label_out_file = open("labels.txt", "w")
    label_out_file.write("\n".join(sorted(typeDict.values())))
    label_out_file.close()

    convert("./cn_trig_ner_arg.train.txt", "train.txt", typeDict)
    convert("./cn_trig_ner_arg.dev.txt", "dev.txt", typeDict)
    convert("./cn_trig_ner_arg.test.txt", "test.txt", typeDict)
