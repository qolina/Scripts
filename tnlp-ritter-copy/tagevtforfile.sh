#!/bin/bash

if [ $# -lt 1 ]; then
    echo 'Usage: sh tagevtforfile.sh inputTextFile [outputevttextFile]'
    exit 0
elif [ $# == 1 ]; then
    input=$1
    output=$1'.evt'
else
    input=$1
    output=$2
    echo 'In/Out files: '$*
fi

echo $input
echo `date`
cat $input | python python/ner/extractEntities2.py --classify --pos --event > $output
