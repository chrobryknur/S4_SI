#!/bin/python3
import itertools
from queue import PriorityQueue

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

for i in range(n):
  for j in range(m):
    if enemyBase[i][j] == 'S':
      possibleStartingPoints.append((i,j))
      enemyBase[i] = enemyBase[i][:j] + " " + enemyBase[i][j+1:]
    if enemyBase[i][j] == 'B':
      possibleStartingPoints.append((i,j))
      enemyBase[i] = enemyBase[i][:j] + "G" + enemyBase[i][j+1:]


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

def endGame(possiblePositions):
  # print(possiblePositions)
  for position in possiblePositions:
    if enemyBase[position[0]][position[1]] != "G":
      return False
  return True



def bfs(v):
  queue = []
  visited = set()
  queue.append((v,0))
  maxDistance = 0
  while len(queue):
    qStart = queue.pop(0)
    vertex = qStart[0]
    distance = qStart[1]
    # print(distance)
    if vertex in visited:
      continue
    visited.add(vertex)
    # print(enemyBase[vertex[0]][vertex[1]])
    if enemyBase[vertex[0]][vertex[1]] == 'G':
      # print(distance)
      if distance > maxDistance:
        maxDistance = distance
    for func in moveFunctions:
      temp = func(vertex)
      if temp != vertex:
        queue.append((temp, distance+1))
  return maxDistance

distances = []

for i in range(1,n-1):
  row=[]
  for j in range(1,m-1):
    row.append(bfs((i,j)))
    # row+=(enemyBase[i][j])
  distances.append(row)
  # print(row)


def heuristic(positions,  parametr):
  maxDist = 0
  for position in positions:
    # print(n,m, position[0], position[1])
    # print(position[1])
    # print("\n")
    temp = distances[position[0]-1][position[1]-1]
    if temp > maxDist:
      maxDist = temp
  return paramatr*maxDist

queue = PriorityQueue()
visited = set()

queue.put((0, possibleStartingPoints, ""))

while not queue.empty():
  currentState = queue.get()
  positions = currentState[1]
  moves = currentState[2]
  if(endGame(positions)):
    output = open('zad_output.txt', 'w')
    output.write(moves)
    # print(moves)
    exit(0)
  
  for direction in [3,2,1,0]:
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
        newPositions.add(moveFunctions[direction](position))
    newPositions = tuple(newPositions)
    if newPositions in visited:
      continue
    visited.add(newPositions)
    # print(newPositions)
    queue.put((len(moves)+heuristic(newPositions), newPositions, moves+directionStr))
