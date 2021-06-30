#!/bin/python3

allWords = set() 


output = open("zad2_output.txt", "w")
output.close()

def chooseBestWords(line):
    DP=[]
    for i in range(len(line)+1):
        DP.append([0,''])
    for i in range(1, len(line)+1):
        lowerBound = max(i-33, -1) # 33 is the length of 'Konstantynopolitańczykowianeczka' so
                                   # there is no need to check for longer words
        word = ''
        j = i-1
        while j > lowerBound:
            word += line[j]
            if word[::-1] in allWords:
                if DP[i][0] < (DP[j][0] + (len(word)**2)):
                    DP[i] = [DP[j][0] + (len(word)**2),DP[j][1] + ' ' + word[::-1]]
            j-=1
    return DP[len(line)][1]


with open('words_for_ai1.txt','r') as f:
        lines = f.readlines()
        for line in lines:
            stripped = line.strip()
            allWords.add(stripped)

with open('zad2_input.txt','r') as file:
    lines = file.readlines()
    output = open("zad2_output.txt","a")
    for line in lines:
        line = line.strip()
        bestPossibleLine = chooseBestWords(line)
        output.write(bestPossibleLine[1:] + "\n")
    output.close() 
