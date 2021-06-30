#!/usr/bin/python3

import time
import random
import chess
import chess.engine
from stockfish import Stockfish

stockfish = Stockfish(parameters={"Threads": 1, "Minimum Thinking Time": 1, "UCI_Elo": 50,
                      "Move Overhead": 1, "Slow Mover": 1, "Skill Level": 1, "Hash": 1, "UCI_Limit Strenth": 'true'})

class Game:
    def __init__(self):
        self.board = chess.Board()
        self.moves_cnt = 0

    def do_move(self, move):
        self.board.push(move)

    def result(self):
        if not self.board.outcome():
            return -100

        if self.board.outcome().winner == chess.WHITE:
            global won
            return 100 - self.moves_cnt
        if self.board.outcome().winner == chess.BLACK:
            global lost
            return -1000

        return -100

    def terminal(self):
        return self.moves_cnt >= 100 or bool(self.board.outcome())

    def random_move(self):
        ms = list(self.board.legal_moves)
        move = random.choice(ms)
        return move

    def agent_move(self):
        startTime = time.time()
        stockfish.set_position(self.board.move_stack)
        result = chess.Move.from_uci(stockfish.get_best_move())
        executionTime = (time.time() - startTime)
        print('Execution time in seconds: ' + str(executionTime))
        self.moves_cnt+=1
        return result


result = 0
games = 50

for i in range(games):
    G = Game()
    while True:
        if G.board.turn:
            m = G.agent_move()
        else:
            m = G.random_move()

        G.do_move(m)
        if G.terminal():
            break
    result += G.result()

print(result)
print(stockfish.default_stockfish_params)
