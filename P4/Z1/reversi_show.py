import random
import sys
from collections import defaultdict as dd

BOK = 50
SX = -100
SY = 0
M = 8

def initial_board():
    B = [ [None] * M for i in range(M)]
    B[3][3] = 1
    B[4][4] = 1
    B[3][4] = 0
    B[4][3] = 0
    return B

    
class Board:
    dirs  = [ (0,1), (1,0), (-1,0), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1) ]
    
    
    def __init__(self):
        self.board = initial_board()
        self.fields = set()
        self.move_list = []
        self.history = []
        for i in range(M):
            for j in range(M):
                if self.board[i][j] == None:   
                    self.fields.add( (j,i) )
                                   
    def moves(self, player):
        res = []
        for (x,y) in self.fields:
            if any( self.can_beat(x,y, direction, player) for direction in Board.dirs):
                res.append( (x,y) )
        if not res:
            return [None]
        return res               
    
    def can_beat(self, x,y, d, player):
        dx,dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x,y) == 1-player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x,y) == player
    
    def get(self, x,y):
        if 0 <= x < M and 0 <=y < M:
            return self.board[y][x]
        return None
                        
    def do_move(self, move, player):
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)
        
        if move == None:
            return
        x,y = move
        x0,y0 = move
        self.board[y][x] = player
        self.fields -= set([move])
        for dx,dy in self.dirs:
            x,y = x0,y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x,y) == 1-player:
              to_beat.append( (x,y) )
              x += dx
              y += dy
            if self.get(x,y) == player:              
                for (nx,ny) in to_beat:
                    self.board[ny][nx] = player
                                                     
    def result(self):
        res = 0
        for y in range(M):
            for x in range(M):
                b = self.board[y][x]                
                if b == 0:
                    res -= 1
                elif b == 1:
                    res += 1
        return res
                
    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] == None 

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return [None]    
    
    def agent_move(self,player):
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        outer_square = [(1, 2), (2, 1), (1, 5), (3, 1), (4, 6), (5, 1), (6, 4), (1, 3), (4, 1), (6, 2), (6, 5), (1, 4), (2, 6), (5, 6), (3, 6), (6, 3)]
        inner_square = [(2, 4), (5, 5), (5, 4), (4, 2), (2, 3), (4, 5), (2, 2), (5, 3), (3, 2), (2, 5), (3, 5), (5, 2)]
        bad = [(0, 1), (7, 1), (6, 1), (1, 1), (6, 6), (0, 6), (6, 7), (1, 7), (7, 6), (6, 0), (1, 0), (1, 6)]

        ms = self.moves(player)
        good_moves = [move for move in ms if move not in bad]

        moves_to_corners = set(corners) & set(good_moves)
        if moves_to_corners:
            return random.choice(list(moves_to_corners))

        moves_to_outer_square = set(outer_square) & set(good_moves)
        if moves_to_outer_square:
            return random.choice(list(moves_to_outer_square))

        moves_to_inner_square = set(inner_square) & set(good_moves)
        if moves_to_inner_square:
            return random.choice(list(moves_to_inner_square))

        if good_moves:
          return random.choice(good_moves)

        return random.choice(ms)

defeats = 0

for i in range(1000):

    player = 0
    B = Board()
    while True:
        if not player:
            m = B.random_move(player)
        else:
            m = B.agent_move(player)
        B.do_move(m, player)
        player = 1-player
        if B.terminal():
            break
    result = B.result()
    if result < 0:
        defeats += 1

print(defeats)
sys.exit(0)                 
