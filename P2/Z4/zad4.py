#!/bin/python3

import random
import itertools

enemyBase = []

inputFile = open('zad_input.txt','r')
lines = inputFile.readlines()

temp = []
for line in lines:
  temp.append(line.strip())
n = len(temp)
m = len(temp[0])

for i in range(n):
  enemyBase.append(temp[i])

def moveLeft(position):
  if enemyBase[position[0]][position[1]-1] != '#':
    return  (position[0], position[1]-1)
  return position

def moveRight(position):
  if enemyBase[position[0]] [position[1]+1] != '#':
    return (position[0], position[1]+1)
    
  return position

def moveUp(position):
  if enemyBase[position[0]-1] [position[1]] != '#':
    return  (position[0]-1, position[1])
  return position

def moveDown(position):
  if enemyBase [position[0]+1] [position[1]]  != '#':
    return  (position[0]+1, position[1])
  return position

moveFunctions = [moveUp, moveDown, moveLeft, moveRight]

possibleStartingPoints =  []
endingPoints = []

for i in range(n):
  for j in range(m):
    if enemyBase[i][j] == 'S':
      possibleStartingPoints.append((i,j))
    if enemyBase[i][j] == 'B':
      possibleStartingPoints.append((i,j))
      endingPoints.append((i,j))

def createNewPositions(oldPositions, direction):
  newPositions = set()
  for position in oldPositions:
    if direction == 'U':
      newPositions.add(moveUp(position))
    if direction == 'D':
      newPositions.add(moveDown(position))
    if direction == 'L':
      newPositions.add(moveLeft(position))
    if direction == 'R':
      newPositions.add(moveRight(position))
  return newPositions


maximumMoves = 64
randomMovesNumber = 16

bestStartingPosition = possibleStartingPoints
bestSequence = ""
allCombinations = list(itertools.permutations(['U','D','L','R']))
for combination in allCombinations:
  sequence  = ""
  for direction in combination:
    for i in range(randomMovesNumber):
      sequence+=direction
  possiblePositionAfterThisTry = possibleStartingPoints
  for direction in sequence:  
    possiblPositionAfterThisTry = createNewPositions(possiblePositionAfterThisTry, direction)

  if len(possiblePositionAfterThisTry) < maximumMoves:
    maximumMoves = len(possiblePositionAfterThisTry)
    bestStartingPosition = possiblePositionAfterThisTry
    bestSequence = sequence

possibleStartingPoints = bestStartingPosition

  

def endGame(possiblePositions):
  for position in possiblePositions:
    if position not in endingPoints:
      return False
  return True

visited = set()

queue = []

queue.append((possibleStartingPoints, ""))

while len(queue):
  currentState  =  queue.pop(0)
  positions = currentState[0]
  moves = currentState[1]

  if(endGame(positions)):
    output = open('zad_output.txt', 'w')
    output.write(bestSequence+moves)
    exit(0)
  for direction in range(4):
    directionStr = ""
    if direction == 0:
      directionStr = "U"
    if direction == 1:
      directionStr = "D"
    if direction == 2:
      directionStr = "L"
    if direction == 3:
      directionStr = "R"
    
    newPositions = set()
    for position in positions:
      possiblePosition = moveFunctions[direction](position)
      if possiblePosition not in newPositions:
        newPositions.add(possiblePosition)
    newPositions = tuple(newPositions)
    if newPositions in visited:
      continue
    if len(newPositions) < len(positions):
      visited.clear()
      queue = [(newPositions, moves+directionStr)]
      visited.add((newPositions))
      break
    queue.append((newPositions, moves+directionStr))
    visited.add(newPositions)












