#!/bin/bash

MODE=1
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

LCOORDS=''
BCOORDS=''
case $MODE in
    1)
        # Default screen
        LCOORDS='750,990'
        BCOORDS='805,345'
    ;;
    2)
        # Right screen (portrait)
        LCOORDS='2250,980'
        BCOORDS='2305,85'
    ;;
    *)
        echo 'unhandled option'
        exit
    ;;
esac

args="bot --letter-coords=$LCOORDS --board-coords=$BCOORDS"
if ! [ $WORD == 0 ]; then
    args="$args --start=$WORD"
fi
if ! [ $LOG == 0 ]; then
    args="-$LOG $args"
fi
args="$args ./res/possible_words.txt"
echo $args

python src/wordle.py $args