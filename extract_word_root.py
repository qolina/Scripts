#!/usr/bin/env python
# -*- coding: utf-8 -*
from __future__ import print_function
import os
import nltk
import sys
import re
import copy
import time
sys.setrecursionlimit(1000000)  # 系统递归深度设置这里设置为一百万
path = os.path.split(os.path.realpath(__file__))[0]


def word_lemma(word_input, pos_input=None):
    if pos_input in ["NN", "NNP", "NNS", "NNPS", "CD", "DT", "FW"]:
        pos_sign = 'n'
    elif pos_input in ["VB", "VBD", "VBG", "VBP", "VBZ"]:
        pos_sign = 'v'
    elif pos_input in ["JJ", "JJR", "JJS"]:
        pos_sign = 'a'
    elif pos_input in ["RB", "RBR", "RBS", "RP"]:
        pos_sign = 'r'
    else:
        pos_sign = None
    try:
        if pos_sign != None:
            word_root = nltk.stem.WordNetLemmatizer().lemmatize(word_input, pos=pos_sign)
        else: 
            word_root = nltk.stem.WordNetLemmatizer().lemmatize(word_input)
    except StandardError as err:
        print(err)
    return(word_root)


    
def word_affix(word_input, pos_input=None):
    affix = ""
    if pos_input != None:
        word_root = word_lemma(word_input, pos_input)
    else:
        word_root = word_lemma(word_input)
    affix = word_input.replace(word_root, '')
    return(affix)


def word_pl(word_input, pos_input=None):
    affix = word_affix(word_input, pos_input)
    if affix != "":
        return("pl")
    else: 
        return("sg")

count = -1
for count, line in enumerate(open(sys.argv[1], 'rU')):
    pass
    count += 1
print(count)
file_out = open(sys.argv[1]+'.rootout','w')
with open(sys.argv[1], 'r') as file_input:
    bar_i = 0
    for line in file_input:
        word_list = []
        word_list_root = []
        word_list_affix = []
        word_list_pl = []
        word_list += line.strip().split(" ")
        for word in word_list:
            word_list_root.append(word_lemma(word,"JJ"))
            word_list_affix.append(word_affix(word))
            word_list_pl.append(word_pl(word))
#        bar_i +=1
#        sys.stdout.flush()
#        sys.stdout.write("Computing: [%s%s] %i%%\r" % ('#' * (bar_i/count*50) , '-' * ((count - bar_i)/count*50) , bar_i / count * 100))
        print("============================",file=file_out)
        print("word_org       %s:" % word_list,file=file_out)
        print("word_root    %s:" % word_list_root,file=file_out)
        print("word_affix   %s:" % word_list_affix,file=file_out)
        print("word_pl      %s:" % word_list_pl,file=file_out)
file_out.close()
