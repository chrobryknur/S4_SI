#!/bin/python3

def opt_dist(seq, D):
    ans = len(seq)
    onesInSequence = 0

    for i in range(len(seq)):
        if seq[i] == 1:
            onesInSequence += 1

    for i in range(len(seq) - D + 1):
        onesInSubsequence = 0
        
        for j in range(i, i + D):
            if seq[j] == 1:
                onesInSubsequence += 1
        onesToFlip = onesInSequence - onesInSubsequence     # ones not in the subsequence
        zeroesToFlip = D - onesInSubsequence                # zeroes in the subsequence

        if onesToFlip + zeroesToFlip < ans:
            ans = onesToFlip + zeroesToFlip

    return ans


output = open('zad4_output.txt','w')
output.close()

input = open('zad4_input.txt','r') 
lines = input.readlines()
for line in lines:
    data = line.split()
    seq = []
    for i in range(len(data[0])):
        if data[0][i] == "1":
            seq.append(1)
        else:
            seq.append(0)
    ans = opt_dist(seq, int(data[1]))
    output = open('zad4_output.txt', 'a')
    output.write(str(ans))
    output.write('\n')



