#!/bin/python3
import itertools
from queue import PriorityQueue
from collections import deque

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


def findWorkersPath(currBoxesPositions, start, end):
    if board[end[0]][end[1]] == 'W':
        return

    if end in currBoxesPositions:
        return

    queue = deque()
    visitedPositions = set()

    queue.append((start, ""))

    while queue:
        vertex = queue.popleft()
        currentPosition = vertex[0]
        currentMoves = vertex[1]

        if currentPosition in currBoxesPositions:
            continue
        if currentPosition == end:
            return currentMoves


        left = moveLeft(currentPosition)
        right = moveRight(currentPosition)
        up = moveUp(currentPosition)
        down = moveDown(currentPosition)

        if ((board[left[0]][left[1]] != 'W') and (left not in visitedPositions)):
            visitedPositions.add(left)
            queue.append((left, currentMoves + "L"))

        if ((board[right[0]][right[1]] != 'W') and (right not in visitedPositions)):
            visitedPositions.add(right)
            queue.append((right, currentMoves + "R"))

        if ((board[up[0]][up[1]] != 'W') and (up not in visitedPositions)):
            visitedPositions.add(up)
            queue.append((up, currentMoves + "U"))

        if ((board[down[0]][down[1]] != 'W') and (down not in visitedPositions)):
            visitedPositions.add(down)
            queue.append((down, currentMoves + "D"))

def generateState(currentBoxesPositions, currentWorkerPosition, currentMoves, currentBoxIndex, direction):
    
    newBoxPosition = None
    workerPositionBeforeMovingTheBox = None
    currBoxPosition = currentBoxesPositions[currentBoxIndex]
    if direction == 'U':
        newBoxPosition = moveUp(currBoxPosition)
        workerPositionBeforeMovingTheBox = moveDown(currBoxPosition)
    if direction == 'D':
        newBoxPosition = moveDown(currBoxPosition)
        workerPositionBeforeMovingTheBox = moveUp(currBoxPosition)
    if direction == 'L':
        newBoxPosition = moveLeft(currBoxPosition)
        workerPositionBeforeMovingTheBox = moveRight(currBoxPosition)
    if direction == 'R':
        newBoxPosition = moveRight(currBoxPosition)
        workerPositionBeforeMovingTheBox = moveLeft(currBoxPosition)

    if board[newBoxPosition[0]][newBoxPosition[1]] == 'W':
        return

    if newBoxPosition in currentBoxesPositions:
        return
    
    pathToTheBox = findWorkersPath(currentBoxesPositions, currentWorkerPosition, workerPositionBeforeMovingTheBox)
    if pathToTheBox is None:
        return
    newBoxesPositions = currentBoxesPositions.copy()
    newBoxesPositions[currentBoxIndex] = newBoxPosition
    

    return (newBoxesPositions, currBoxPosition,  currentMoves + pathToTheBox + direction)


def endGame(possibleBoxesPositions):
  for position in possibleBoxesPositions:
    if position not in boxesGoalPoints:
      return False
  return True

def manhattanDistance(positionA, positionB):
    return abs(positionA[0] - positionB[0]) + abs(positionA[1] - positionB[1])

def heuristic(possibleBoxesPositions):
    result = 0
    goals = boxesGoalPoints.copy()

    for boxPosition in possibleBoxesPositions:
        minDistance = 99999
        distances = []
        goalToRemove = None

        for goal in goals:
            distances.append(manhattanDistance(goal, boxPosition))

        for distance in distances:
            if distance < minDistance:
                minDistance = distance

        for goal in goals:
            if manhattanDistance(goal, boxPosition) == minDistance:
                goalToRemove = goal
                break

        goals.remove(goalToRemove)
        result+=minDistance
    return result


def solveSokoban():
    queue = PriorityQueue()
    visited = set()

    queue.put((heuristic(boxesPositions), boxesPositions, startingPosition, ""))
    visited.add((tuple(sorted(boxesPositions)), startingPosition))

    while not queue.empty():
        currentState = queue.get()
        currentBoxesPositions = currentState[1]
        currentWorkerPosition = currentState[2] 
        currentMoves = currentState[3]

        if(endGame(currentBoxesPositions)):
            output = open('zad_output.txt', 'w')
            output.write(currentMoves)
            exit(0)
        
        for directionStr in ['U','D','L','R']:
            for boxIndex in range(len(currentBoxesPositions)):
                nextState = generateState(currentBoxesPositions, currentWorkerPosition, currentMoves, boxIndex, directionStr)
                if (nextState is not None) and ((tuple(sorted(nextState[0])), nextState[1]) not in visited):
                    visited.add((tuple(sorted(nextState[0])), nextState[1]))
                    queue.put((heuristic(nextState[0]), nextState[0], nextState[1], nextState[2]))


solveSokoban()