#!/usr/local/bin/python3.8

import random

inputFile=open("zad5_input.txt", "r")
outputFile=open("zad5_output.txt", "w")
outputFile.close()
outputFile=open("zad5_output.txt", "a")

rawData=inputFile.readlines()

rows=int(rawData[0].split()[0])
cols=int(rawData[0].split()[1])

rowD=[]
columnD=[]

smallChance=0.2

maxIterations = 1000000

for i in range(1, rows+1):
    rowD.append(int(rawData[i]))

for i in range(rows+1, rows+cols+1):
    columnD.append(int(rawData[i]))

image=[]

for i in range(rows):
    row=[]
    for j in range(cols):
        row.append(0)
    image.append(row)

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


def newImage():
    for i in range(cols):
        for j in range(rows):
            image[i][j] = 0



def getRow(n): # returns the nth row from image
    row=[]
    for i in range(cols):
        row.append(image[i][n])
    return row

def badRows():
    bad=[]
    for i in range(rows):
        if opt_dist(getRow(i), rowD[i]): # row is not optimal
            bad.append(i)
    return bad

def badCols():
    bad=[]
    for i in range(cols):
        if opt_dist(image[i], columnD[i]): # column is not optimal
            bad.append(i)
    return bad

iterations = 0

while badCols() or badRows():
    
    if iterations > maxIterations:
        iterations = 0
        newImage()
        continue

    iterations += 1

    bCols=badCols()
    bRows=badRows()
    if (random.randint(0,1) and bRows) or not bCols: # select a random row and choose a column which improvement makes the biggest change
        randRow = bRows[random.randint(0, len(bRows)-1)]
        mostOptimal = rows*cols
        bestColumn = 0
        prevRowOptDist=opt_dist(getRow(randRow), rowD[randRow])
        for i in range(cols):
            prevColOptDist = opt_dist(image[i], columnD[i])
            image[i][randRow] = not image[i][randRow] # flip a pixel
            newColOptDist = opt_dist(image[i], columnD[i])
            newRowOptDist=opt_dist(getRow(randRow), rowD[randRow])

            prevOpt = prevRowOptDist + prevColOptDist
            newOpt = newRowOptDist + newColOptDist

            if newOpt < prevOpt and newOpt < mostOptimal:
                mostOptimal = newOpt
                bestColumn = i
            image[i][randRow] = not image[i][randRow] # restore pixel's previous state

        if random.random() < smallChance:
            bestColumn = random.randint(0, cols-1)

        image[bestColumn][randRow] = not image[bestColumn][randRow] # change the best pixel
    
    elif bCols:
        randCol = bCols[random.randint(0, len(bCols)-1)]
        mostOptimal = rows*cols
        bestRow = 0
        prevColOptDist = opt_dist(image[randCol], columnD[randCol])
        for i in range(rows):
            prevRowOptDist = opt_dist(getRow(i), rowD[i])
            image[randCol][i] = not image[randCol][i]
            newColOptDist = opt_dist(image[randCol], columnD[randCol])
            newRowOptDist = opt_dist(getRow(i), rowD[i])

            prevOpt = prevRowOptDist + prevColOptDist
            newOpt = newRowOptDist + newColOptDist

            if newOpt < prevOpt and newOpt < mostOptimal:
                mostOptimal = newOpt
                bestRow = i
            image[randCol][i] = not image[randCol][i]
        if random.random() < smallChance:
            bestRow = random.randint(0, rows-1)
            
        image[randCol][bestRow] = not image[randCol][bestRow]

for i in range(rows):
    line=""
    for j in range(cols):
        if image[j][i]:
            line+="#"
        else:
            line+="."
    line+="\n"
    outputFile.write(line)
