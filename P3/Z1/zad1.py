#!/usr/bin/python3

rowLength=0
columnLength=0
rows = []
columns = []
notSolvedPixels = []
allPossibleRowBitmaps = []
allPossibleColumnBitmaps = []
nonogram = []

def readInput():
    inputFile = open('zad_input.txt', 'r')
    inputLines = inputFile.readlines()

    global rowLength
    global columnLength

    rowLength,columnLength = map(int, inputLines[0].strip().split())

    for i in range(rowLength):
        rows.append(list(map(int, inputLines[i+1].strip().split())))

    for j in range(columnLength):
        columns.append(list(map(int, inputLines[rowLength+1+j].strip().split())))

def prepareEmptyNonogram():
    for i in range(rowLength):
        for j in range(columnLength):
            notSolvedPixels.append((j, i))

    for i in range(rowLength):
        nonogram.append([])
        for j in range(columnLength):
            nonogram[i].append(0)


def generateAllPossibleBitmaps(lengthOfBitmap, allBlocksInBitmap, currentBlockIndex, firstPossibleStartingPoint):
    possibleBitmaps = []
    
    if currentBlockIndex == len(allBlocksInBitmap):
        possibleBitmaps.append([])
        for i in range(firstPossibleStartingPoint, lengthOfBitmap+1):
            possibleBitmaps[0].append(0)
        return possibleBitmaps
    
    elif allBlocksInBitmap[currentBlockIndex] + firstPossibleStartingPoint > lengthOfBitmap:
        return 0

    else:
        startingPoint = firstPossibleStartingPoint
        while startingPoint <= lengthOfBitmap - allBlocksInBitmap[currentBlockIndex]:
            newBlockIndex = currentBlockIndex+1
            newStartingPoint = startingPoint + allBlocksInBitmap[currentBlockIndex] + 1
            newPossibleBitmaps = generateAllPossibleBitmaps(lengthOfBitmap, allBlocksInBitmap, newBlockIndex, newStartingPoint)
            if newPossibleBitmaps:
                for bitmap in newPossibleBitmaps:
                    newBitmap = []
                    for i in range(firstPossibleStartingPoint, startingPoint):
                        newBitmap.append(0)
                    for i in range(allBlocksInBitmap[currentBlockIndex]):
                        newBitmap.append(1)
                    if currentBlockIndex != (len(allBlocksInBitmap) - 1):
                        newBitmap.append(0)
                    newBitmap+=bitmap
                    possibleBitmaps.append(newBitmap)
            startingPoint+=1
    return possibleBitmaps

def generateBitmaps():
    for row in rows:
        bitmaps = generateAllPossibleBitmaps(columnLength, row, 0, 0)
        allPossibleRowBitmaps.append(bitmaps)

    for column in columns:
        bitmaps = generateAllPossibleBitmaps(rowLength, column, 0, 0)
        allPossibleColumnBitmaps.append(bitmaps)

def fixPixel(x, y):
    rowBitmaps    = allPossibleRowBitmaps[y]
    columnBitmaps = allPossibleColumnBitmaps[x]

    pixelValue    = rowBitmaps[0][x]
    pixelsValueIsKnown = True

    for bitmap in rowBitmaps:
        if bitmap[x] != pixelValue:
            pixelsValueIsKnown = False

    if pixelsValueIsKnown:
        nonogram[y][x] = pixelValue
        newPossibleColumnBitmaps = []
        for bitmap in allPossibleColumnBitmaps[x]:
            if bitmap[y] == pixelValue:
                newPossibleColumnBitmaps.append(bitmap)
        allPossibleColumnBitmaps[x] = newPossibleColumnBitmaps

    pixelValue = columnBitmaps[0][y]
    pixelsValueIsKnown = True

    for bitmap in columnBitmaps:
        if bitmap[y] != pixelValue:
            pixelsValueIsKnown = False

    if pixelsValueIsKnown:
        nonogram[y][x] = pixelValue
        newPossibleRowBitmaps = []

        for bitmap in allPossibleRowBitmaps[y]:
            if bitmap[x] == pixelValue:
                newPossibleRowBitmaps.append(bitmap)
        allPossibleRowBitmaps[y] = newPossibleRowBitmaps
    else:
        notSolvedPixels.append((x,y))

def printOutput():
    outputFile = open("zad_output.txt","w")
    for row in nonogram:
        rowString = ""
        for bit in row:
            if bit:
                rowString+="#"
            else:
                rowString+="."
        rowString+="\n"
        outputFile.write(rowString)

def solveNonogram():
    while notSolvedPixels:
        pixelToSolve = notSolvedPixels.pop(0)
        fixPixel(pixelToSolve[0], pixelToSolve[1])

def main():
    readInput()
    prepareEmptyNonogram()
    generateBitmaps()
    solveNonogram()
    printOutput()

if __name__ == "__main__":
    main()
