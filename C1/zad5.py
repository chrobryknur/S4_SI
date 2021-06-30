#!/bin/python3
import random
from itertools import combinations

bcards=[]
fcards=[]

def handScore(hand):
    sameColor = True
    color = hand[0][1]
    for i in range (1, 5):
        if hand[i][1] != color:
            sameColor = False
    hand = sorted(hand, key= lambda x: x[0])
    straight = True
    for i in range (0, 4):
        if hand[i+1][0] - hand[i][0] != 1:
            straight = False

    sameCards = []
    for i in range(11):
        sameCards.append(0)
    for i in range(0, 5):
        sameCards[hand[i][0]]+=1

    pairs = 0
    threes = 0
    fourths = 0

    for i in range(len(sameCards)):
        if sameCards[i] == 2:
            pairs += 1
        if sameCards[i] == 3:
            threes += 1
        if sameCards[i] == 4:
            fourths += 1

    if straight and sameColor:
        return 8
    if fourths:
        return 7
    if threes and pairs:
        return 6
    if sameColor:
        return 5
    if straight:
        return 4
    if threes:
        return 3
    if pairs == 2:
        return 2
    if pairs:
        return 1
    return 0


def compareHands(bhand, fhand):
    bScore = handScore(bhand)
    fScore = handScore(fhand)

    if bScore > fScore:
        return 1
    return 0




def init():
    for card in range(2, 11):
        for color in range(0,4):
            bcards.append([card, color])

    for card in range(0, 4):
        for color in range(0,4):
            fcards.append([card, color])



def playAllPossibleGames():
    B = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    F = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for hand in combinations(bcards, 5):
        B[handScore(hand)]+=1
    for hand in combinations(fcards, 5):
        F[handScore(hand)]+=1
    
    bWins = 0

    for i in range(2, 10):
        for j in range(1, i):
            bWins += B[i] * F[j]

    games = 1646701056

    print(bWins / games)



init()
playAllPossibleGames()
