
import sys
from collections import Counter

paperFilenames = []
paperFilenames.append(sys.argv[1])

def statIjcai17(filename):
    content = open(filename, "r").readlines()
    content = [line.strip() for line in content]

    paperIds = [int(line[line.find(":")+1:]) for line in content if line.startswith("PaperID")]
    titles = [line[line.find(":")+1:] for line in content if line.startswith("Title")]
    tracks = [line[line.find(":")+1:] for line in content if line.startswith("Track")]
    authors = [line[line.find(":")+1:].split(",") for line in content if line.startswith("Author")]

    print "-- #Paper",len(paperIds)
    print "-- #paperInTrack", Counter(tracks).most_common()
    print statAuthors(authors)


def statAuthors(authors):
    firstAuthors = [arr[0] for arr in authors]
    fstAuCounter = Counter(firstAuthors)
    paperNumEachAuthor = Counter(fstAuCounter.values())
    authorPaperNum = [(item[1], item[0]) for item in paperNumEachAuthor.most_common()]
    print "(author, firstAuthorPaperNum)", authorPaperNum
    print "-- First authors"
    for item in fstAuCounter.most_common()[:100]:
        print item[0], "\t", item[1]

if __name__ == "__main__":
    print "Usage: python statPaper.py paperFilename1"

    statIjcai17(paperFilenames[0])
