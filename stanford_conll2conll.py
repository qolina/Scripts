
# from seven column conll file to standard 10 columns conll
import sys

content = file(sys.argv[1], "r").readlines()

for line in content:
    arr = line.strip().split("\t")
    if len(arr) != 7: print line.strip()
    else:
        new_arr = arr[:4] + [arr[3], arr[4], "0", "ROOT", arr[4], arr[4]]
        print "\t".join(new_arr)
