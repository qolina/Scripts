#!/bin/bash

if [ $# -lt 2 ]; then
    echo 'Usage: sh qnerpos.sh inputTextFile outputNERtextFile'
    exit 0
else
    input=$1
    output=$2
    echo 'In/Out files: '$*
fi

export TWITTER_NLP=./
cat $input | python python/ner/extractEntities2.py --classify --pos > $output
