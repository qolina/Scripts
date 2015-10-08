# convert conll formatted sentence (may have multiple root) to a Tree in NLTK
# input: conll formatted sentence;
# output: Trees
from nltk.tree import ParentedTree
import sys
import re


def conll2tree(arr):
    #format: idx, word, _, pos, pos, _, head, _, _, _

    # dep:head
    dep2headHash = {}
    for wArr in arr:
        dep2headHash[int(wArr[0])] = int(wArr[6])
    #print dep2headHash


    # head:depsList[]
    head2depsHash = {} 
    for dep in dep2headHash:
        head = dep2headHash[dep]

        if head in head2depsHash:
            head2depsHash[head].append(dep)
        else:
            head2depsHash[head] = [dep]
    #print head2depsHash

#    if len(head2depsHash[0]) > 1:
#        print "Error. Multiple roots."

    # head:tree
    treeheadHash = {}
    for head in head2depsHash:
        tree = ParentedTree(head, head2depsHash[head])
        treeheadHash[head] = tree

    root = updateTree(treeheadHash, 0)
    return root


def updateTree(treeheadHash, idx):
    #print idx, "pre", treeheadHash[idx]
    children = []
    for child in treeheadHash[idx]:
        if child in treeheadHash:
            children.append(updateTree(treeheadHash, child))
        else:
            children.append(child)
    treeheadHash[idx] = ParentedTree(idx, children)
    #print idx, "aft", treeheadHash[idx]
    return treeheadHash[idx]


def getChildren(root):
    childrenTree = []
    for child in root:
        childrenTree.append(child)
    return childrenTree


def getTag(senArr, root):
    return senArr[int(root.label())][3]


if __name__ == "__main__":
    senArr_eg = ["1	I	_	NN	NN	_	2	_	_	_", 
                "2	love	_	VB	VB	_	0	_	_	_", 
                "3	to	_	TO	TO	_	4	_	_	_", 
                "4	eat	_	VB	VB	_	2	_	_	_", 
                "5	cabbage	_	NN	NN	_	4	_	_	_"]

    print "****input_example:"
    print "\n".join(senArr_eg)

    senArr_eg = [line.split("\t") for line in senArr_eg]
    root = conll2tree(senArr_eg)
    print "****tree", root
    print "****height", root.height()
    print "root.label", root.label()

    print root[0]
    children_of_root = getChildren(root)
    for child in children_of_root:
        print "*** child of root", child.label()
        print "tree position", ParentedTree.treeposition(child)
        print "parent", ParentedTree.parent(child)
        print "parent_idx", ParentedTree.parent_index(child)
        print root[ParentedTree.parent_index(child)]


