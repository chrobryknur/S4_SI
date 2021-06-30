#!/usr/bin/python3

import random
import chess
from queue import PriorityQueue
from itertools import count
import time

pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


class Game:
    def __init__(self):
        self.board = chess.Board()
        self.moves_cnt = 0

    def do_move(self, move):
        self.board.push(move)

    def result(self):
        if not self.board.outcome(): # >= 100 moves
            return -100

        if self.board.outcome().winner == chess.WHITE:
            return 100 - self.moves_cnt
        if self.board.outcome().winner == chess.BLACK:
            return -1000

        return -100

    def terminal(self):
        return self.moves_cnt >= 100 or bool(self.board.outcome())

    def random_move(self):
        ms = list(self.board.legal_moves)
        move = random.choice(ms)
        return move

    def evaluate_board(self):
        startTime = time.time()
        if self.board.is_checkmate():
            return 9999
        if self.board.is_stalemate():
            return -100
        if self.board.is_insufficient_material():
            return -100

        wp = len(self.board.pieces(chess.PAWN, chess.WHITE))
        bp = len(self.board.pieces(chess.PAWN, chess.BLACK))
        wn = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(self.board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(self.board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(self.board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(self.board.pieces(chess.ROOK, chess.WHITE))
        br = len(self.board.pieces(chess.ROOK, chess.BLACK))
        wq = len(self.board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(self.board.pieces(chess.QUEEN, chess.BLACK))

        material = 100 * (wp - bp) + 300 * (wn - bn) + 300 * \
            (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

        white_pawns_score = sum(
            [pawntable[i] for i in self.board.pieces(chess.PAWN, chess.WHITE)])
        black_pawns_score = sum([-pawntable[chess.square_mirror(i)]
                                for i in self.board.pieces(chess.PAWN, chess.BLACK)])

        white_knights_score = sum(
            [knightstable[i] for i in self.board.pieces(chess.KNIGHT, chess.WHITE)])
        black_knights_score = sum([-knightstable[chess.square_mirror(i)]
                                  for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])

        white_bishops_score = sum(
            [bishopstable[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])
        black_bishops_score = sum([-bishopstable[chess.square_mirror(i)]
                                  for i in self.board.pieces(chess.BISHOP, chess.BLACK)])

        white_rooks_score = sum(
            [rookstable[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)])
        black_rooks_score = sum([-rookstable[chess.square_mirror(i)]
                                for i in self.board.pieces(chess.ROOK, chess.BLACK)])

        white_queens_score = sum(
            [queenstable[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)])
        black_queens_score = sum([-queenstable[chess.square_mirror(i)]
                                 for i in self.board.pieces(chess.QUEEN, chess.BLACK)])

        white_kings_score = sum(
            [kingstable[i] for i in self.board.pieces(chess.KING, chess.WHITE)])
        black_kings_score = sum([-kingstable[chess.square_mirror(i)]
                                for i in self.board.pieces(chess.KING, chess.BLACK)])

        eval = material
        eval += white_pawns_score + white_knights_score + white_bishops_score + \
            white_rooks_score + white_queens_score + white_kings_score
        eval -= black_pawns_score + black_knights_score + black_bishops_score + \
            black_rooks_score + black_queens_score + black_kings_score

        executionTime = (time.time() - startTime)
        print('Execution time in seconds: ' + str(executionTime))

        return eval

    def agent_move(self):
        ms = self.board.legal_moves
        self.moves_cnt += 1

        queue = PriorityQueue()
        unique = count()

        for move in ms:
            self.board.push(move)
            t = (-self.evaluate_board(), next(unique), move)
            self.board.pop()
            queue.put(t)

        best_move = queue.get()
        return best_move[2]


result = 0
games = 50

for i in range(games):
    player = 1
    G = Game()
    while True:
        if G.board.turn:
            m = G.agent_move()
        else:
            m = G.random_move()

        player = not player

        G.do_move(m)
        if G.terminal():
            break
    result += G.result()

print(result)
