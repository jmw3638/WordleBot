#!/bin/bash

MODE=2
LOG=0
WORD=0
mode_re='^[0-9]+$'
log_re='^v+$'
word_re='^[a-zA-Z]{5}$'
if [ $1 ]; then
    if [[ $1 =~ $mode_re ]]; then
        MODE=$1
    elif [[ $1 =~ $log_re ]]; then
        LOG=$1
    elif [[ $1 =~ $word_re ]]; then
        WORD=$1
    fi
fi
if [ $2 ]; then
    if [[ $2 =~ $mode_re ]]; then
        MODE=$2
    elif [[ $2 =~ $log_re ]]; then
        LOG=$2
    elif [[ $2 =~ $word_re ]]; then
        WORD=$2
    fi
fi
if [ $3 ]; then
    if [[ $3 =~ $mode_re ]]; then
        MODE=$3
    elif [[ $3 =~ $log_re ]]; then
        LOG=$3
    elif [[ $3 =~ $word_re ]]; then
        WORD=$3
    fi
fi
echo 'mode:' $MODE

COORDS=''
case $MODE in
    1)
        # Laptop screen (3 monitors)
        COORDS='-1170,990'
    ;;
    2)
        # Default screen
        COORDS='750,990'
    ;;
    3)
        # Right screen (portrait)
        COORDS='2250,980'
    ;;
    *)
        echo 'unhandled option'
        exit
    ;;
esac

args="--coords=$COORDS"
if ! [ $WORD == 0 ]; then
    args="$args --start=$WORD"
fi
if ! [ $LOG == 0 ]; then
    args="$args -$LOG"
fi
echo $args

python wordle.py $args