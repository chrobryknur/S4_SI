#!/bin/python3
import itertools
from queue import PriorityQueue

board = []

inputFile = open('zad_input.txt','r')
lines = inputFile.readlines()

temp = []
for line in lines:
  temp.append(line.strip())
rows = len(temp)
cols = len(temp[0])

for i in range(rows):
  board.append(temp[i])

boxesGoalPoints = []
boxesPositions = []
startingPosition = (0,0)

def moveLeft(position):
    return  (position[0], position[1]-1)

def moveRight(position):
    return (position[0], position[1]+1)

def moveUp(position):
    return  (position[0]-1, position[1])

def moveDown(position):
    return  (position[0]+1, position[1])

for i in range(rows):
    for j in range(len(board[0])):
        if board[i][j] == 'K':
            startingPosition = (i,j)
        if board[i][j] == 'B':
            boxesPositions.append((i,j))
        if board[i][j] == 'G':
            boxesGoalPoints.append((i,j))
        if board[i][j] == '*':
            boxesPositions.append((i,j))
            boxesGoalPoints.append((i,j))
        if board[i][j] == '+':
            startingPosition = (i,j)
            boxesGoalPoints.append((i,j))

def generateMove(currPosition, currBoxesPositions, moves, direction):
    firstMove = None
    secondMove = None
    if direction == 'U':
        firstMove = moveUp(currPosition)
        secondMove = moveUp(firstMove)
    if direction == 'D':
        firstMove = moveDown(currPosition)
        secondMove = moveDown(firstMove)
    if direction == 'L':
        firstMove = moveLeft(currPosition)
        secondMove = moveLeft(firstMove)
    if direction == 'R':
        firstMove = moveRight(currPosition)
        secondMove = moveRight(firstMove)

    if board[firstMove[0]][firstMove[1]] == 'W':
        return
    
    if firstMove in currBoxesPositions:
        if board[secondMove[0]][secondMove[1]] != 'W' and secondMove not in currBoxesPositions:
            newBoxesPositions = []
            for boxPosition in currentBoxesPositions:
                if boxPosition == firstMove:
                    newBoxesPositions.append(secondMove)
                else:
                    newBoxesPositions.append(boxPosition)
            return(firstMove, newBoxesPositions, moves+direction)

        else:
            return
    
    return (firstMove, currBoxesPositions, moves+direction)


def endGame(possibleBoxesPositions):
  for position in possibleBoxesPositions:
    if position not in boxesGoalPoints:
      return False
  return True

def heuristic(possibleBoxesPositions):
    maxDist = 99999
    for boxPositions in itertools.permutations(possibleBoxesPositions):
        temp = 0
        for i in range(len(boxesGoalPoints)):
            temp+=abs(boxPositions[i][0]-boxesGoalPoints[i][0])+abs(boxPositions[i][1]-boxesGoalPoints[i][1])
        if temp < maxDist:
            maxDist = temp
    return maxDist

queue = PriorityQueue()
visited = set()

queue.put((heuristic(boxesPositions), startingPosition, boxesPositions, ""))


while not queue.empty():
    currentState = queue.get()
    currentPosition = currentState[1] 
    currentBoxesPositions = currentState[2]
    currentMoves = currentState[3]

    if (currentPosition, tuple(sorted(currentBoxesPositions))) in  visited:
        continue
    visited.add((currentPosition, tuple(sorted(currentBoxesPositions))))

    if(endGame(currentBoxesPositions)):
        output = open('zad_output.txt', 'w')
        output.write(currentMoves)
        exit(0)
    
    for directionStr in ["U","D","L","R"]:
        nextState = generateMove(currentPosition, currentBoxesPositions, currentMoves, directionStr)
        if nextState is not None and (nextState[0], tuple(sorted(nextState[1]))) not in visited:
            queue.put((len(nextState[2]) + heuristic(nextState[1]), nextState[0], nextState[1], nextState[2]))

