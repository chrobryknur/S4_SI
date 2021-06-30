#!/bin/bash

for i in $(seq 3)
do
        python3 sudoku.py < e$i > e$i.pl
        
        printf "Test $i\n"

        output=$(swipl -c e$i.pl 2>/dev/null | tr -d '[]' | sed 's/,/ /g')

        printf "\n"
        
        iterator=0
        touch out$i
        for number in $output
        do
                printf $number >> out$i
                iterator=$((iterator+1)) 
                [ "$iterator" -eq 9 ] && iterator=0 && printf "\n" >> out$i

        done

        diff -y e$i out$i
        printf "\n"
done

rm -f out* a.out *.pl
