import sys

def uniq(filename):
    content = file(filename, "r").readlines()
    contentHash = dict([(line.strip(), 0) for line in content])
    #print "\n".join(sorted(contentHash.keys()))
    return contentHash

########### main
if __name__ == "__main__":
    nolabelGram = uniq(sys.argv[1])
    sys.exit(0)
    nolabelGram = [item.replace(" ", "_") for item in nolabelGram]

    content = file(sys.argv[2], "r").readlines()
    labelGram = [line.strip().split(" ") for line in content ]
    labelGram = dict([(item[1], item[0]) for item in labelGram])

    commonGram = [gram+" "+labelGram[gram] for gram in nolabelGram if gram in labelGram]
    print len(commonGram)
    print "\n".join(commonGram)
