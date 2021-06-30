#!/bin/bash

[ -z $1 ] && echo "No argument" && exit

for i in $(seq $1)
do
        printf "Run $i: "
        result=$(python3 reversi_show.py)
        [ "$result" -ge 70 ] && echo "Failure: $result defeats" && exit
        printf "\t$result defeats\n"
done
