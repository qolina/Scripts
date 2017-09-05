for i in `ls $1`
do
    echo "sh tagevtforfile.sh "$1$i
#    if [ -f $1$i]
#    then
#        echo '-f'
#    fi
done
