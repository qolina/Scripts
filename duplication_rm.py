import sys

content = file(sys.argv[1], "r").readlines()

contentHash = dict([(line, 1) for line in content])

print contentHash.keys()[:3]
