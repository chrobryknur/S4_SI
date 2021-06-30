#!/bin/python3

# THIS DOES NOT WORK

visited = []

def HashPosition(board):
    text=str(board.bKing[0])+str(board.bKing[1])
    text+=str(board.wKing[0])+str(board.wKing[1])
    text+=str(board.wRook[0])+str(board.wRook[1])
    return text 

class state:
    def __init__(self, bKing, wKing, wRook, turn, depth, rookMoves, prevState):
        self.bKing = bKing
        self.wKing = wKing
        self.wRook = wRook
        self.turn  = turn
        self.depth = depth
        self.rookMoves = rookMoves
        self.prevState = prevState

    def inCheck(self):
        return self.bKing[0] == self.wRook[0] or self.bKing[1] == self.wRook[1]
    
    def kingDefendingRook(self):
        return (abs(self.wKing[0] - self.wRook[0])<=1) and (abs(self.wKing[1]-self.wRook[1]) <=1)
    
    def rookCanBeCaptured(self):
        return (abs(self.bKing[0] - self.wRook[0]) <=1) and (abs(self.bKing[1]-self.wRook[1])<=1) and not self.kingDefendingRook()

    def checkmate(self):
        return self.inCheck() and not self.rookCanBeCaptured() 

    def correctPosition(self):
        if self.wKing[0] == self.wRook[0] and self.wKing[1] == self.wRook[1]:
            return False
        if self.wRook[0] == self.bKing[0] and self.wRook[1] == self.bKing[1]:
            return False
        if abs(self.wKing[0] - self.bKing[0]) <= 1 and abs(self.wKing[1] - self.bKing[1]) <= 1:
            return False
        if self.wKing[0] not in range(1, 9) or self.wKing[1] not in range(1, 9):
            return False
        if self.wRook[0] not in range(1, 9) or self.wRook[1] not in range(1, 9):
            return False
        if self.bKing[0] not in range(1, 9) or self.bKing[1] not in range(1, 9):
            return False
        return True

    def possibleNextStates(self):
        states = []
        if self.turn == 0: # white
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == j and i == 0:
                        continue
                    newKingPos = (self.wKing[0]+i, self.wKing[1]+j)
                    newState = state(self.bKing, newKingPos, self.wRook, not self.turn, self.depth+1, self.rookMoves, HashPosition(self))
                    if newState.correctPosition():
                        states.append(newState)
            if self.rookMoves < 3: # we need to limit maximum rook moves, because it would be too much possible moves to check
                for i in range(1, 9):
                    if i != self.wRook[0]:
                        newRookPos = (i, self.wRook[1])
                        newState = state(self.bKing, self.wKing, newRookPos, not self.turn, self.depth+1, self.rookMoves+1, HashPosition(self))
                        if newState.correctPosition():
                            states.append(newState)
                    if i != self.wRook[1]:
                        newRookPos = (self.wRook[0], i)
                        newState = state(self.bKing, self.wKing, newRookPos, not self.turn, self.depth+1, self.rookMoves+1, HashPosition(self))
                        if newState.correctPosition():
                            states.append(newState)
        else:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == j and i == 0:
                        continue
                    newKingPos = (self.bKing[0]+i, self.bKing[1]+j)
                    newState = state(newKingPos, self.wKing, self.wRook, not self.turn, self.depth+1, self.rookMoves, HashPosition(self))
                    if newState.correctPosition() and not newState.inCheck():
                        states.append(newState)

        return states



def FindSolution(startingState):
    queue = []
    queue.append(startingState)
    visited = []
    visited.append(HashPosition(startingState))
    while queue:
        currState=queue[0]
        queue.pop(0)
        nextStates = currState.possibleNextStates()
        if not nextStates and currState.checkmate():
            print(HashPosition(currState))
            return currState.depth
        for stat in nextStates:
            stateHash = HashPosition(stat)
            if stateHash not in visited and stat.depth < 11:
                visited.append(stateHash)
                queue.append(stat)
    

with open('zad1_input.txt', 'r') as file:
    lines =  file.readlines()
    tests = []
    for test in lines:
        tests.append(test.strip().split())
    for test in tests:
        bKing = (ord(test[3][0])-96, int(test[3][1]))
        wKing = (ord(test[1][0])-96, int(test[1][1]))
        wRook = (ord(test[2][0])-96, int(test[2][1]))
        startingState = state(bKing, wKing, wRook, test[0] == "black", 0, 0,"start")
        score = FindSolution(startingState)
        output = open("zad1_output.txt","w")
        output.write(str(score)) 
        output.close() 
                




