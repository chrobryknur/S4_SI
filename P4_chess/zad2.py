#!/usr/bin/python3

import random
import chess
from queue import PriorityQueue
from itertools import count
from stockfish import Stockfish

stockfish = Stockfish()


class Weights:
    def __init__(self):
        self.PAWN = 1
        self.KNIGHT = random.randint(0, 10)
        self.BISHOP = random.randint(0, 10)
        self.ROOK = random.randint(0, 10)
        self.QUEEN = random.randint(0, 10)

    def print_weights(self):
        output_string = "Weights: "
        output_string += str(self.PAWN) + " " + str(self.KNIGHT) + " "
        output_string += str(self.BISHOP) + " " + str(self.ROOK) + " "
        output_string += str(self.QUEEN)
        return output_string


class Agent:
    def __init__(self, id):
        self.weights = Weights()
        self.alpha = random.random()
        self.score = 0
        self.id = id
        self.wins = 0

    def evaluate_board(self, board, legal_moves):
        if board.is_checkmate():
            return 9999

        wp = len(board.pieces(chess.PAWN, not board.turn))
        bp = len(board.pieces(chess.PAWN, board.turn))
        wn = len(board.pieces(chess.KNIGHT, not board.turn))
        bn = len(board.pieces(chess.KNIGHT, board.turn))
        wb = len(board.pieces(chess.BISHOP, not board.turn))
        bb = len(board.pieces(chess.BISHOP, board.turn))
        wr = len(board.pieces(chess.ROOK, not board.turn))
        br = len(board.pieces(chess.ROOK, board.turn))
        wq = len(board.pieces(chess.QUEEN, not board.turn))
        bq = len(board.pieces(chess.QUEEN, board.turn))

        material = self.weights.PAWN * \
            (wp - bp) + self.weights.KNIGHT * (wn - bn)
        material += self.weights.BISHOP * \
            (wb - bb) + self.weights.ROOK * \
            (wr - br) + self.weights.QUEEN * (wq - bq)

        enemy_legal_moves = len(list(board.legal_moves))

        eval = material + self.alpha * (legal_moves - enemy_legal_moves)
        return eval

    def best_move(self, board):
        ms = board.legal_moves

        if random.random() < 0.05:
            return random.choice(list(ms))

        queue = PriorityQueue()
        unique = count()

        for move in ms:
            legal_moves = len(list(board.legal_moves))
            board.push(move)
            t = (-self.evaluate_board(board, legal_moves), next(unique), move)
            board.pop()
            queue.put(t)

        best_move = queue.get()
        return best_move[2]

    def update_score(self, score):
        if score == 1:
            self.wins += 1
        self.score += score

    def print(self):
        print("Agent " + str(self.id))
        print("Score: " + str(self.score))
        print("Wins: " + str(self.wins))
        print(self.weights.print_weights())
        print("Alpha: " + str(self.alpha)+"\n")


class Game:
    def __init__(self, white, black):
        self.board = chess.Board()
        self.moves_cnt = 0
        self.white = white
        self.black = black

    def do_move(self, move):
        self.board.push(move)

    def result(self):
        stockfish.set_fen_position(self.board.fen())
        result = stockfish.get_evaluation()
        if result["value"] > 0:
            return (1, 0)
        elif result["value"] == 0:
            return (0.5, 0.5)
        return (0, 1)

    def terminal(self):
        return self.moves_cnt >= 100 or bool(self.board.outcome())

    def play(self):
        while True:
            if self.board.turn:
                self.do_move(self.white.best_move(self.board))
                self.moves_cnt += 1
            else:
                self.do_move(self.black.best_move(self.board))

            if self.terminal():
                break

        return self.result()


class Simulation:
    def __init__(self, agents_num):
        self.agents = []
        self.agents_num = agents_num
        for id in range(self.agents_num):
            self.agents.append(Agent(id))
        self.run()
        self.print_results()

    def run(self):
        for i in range(self.agents_num):
            for j in range(self.agents_num):
                if i != j:
                    G = Game(self.agents[i], self.agents[j])
                    result = G.play()
                    self.agents[i].update_score(result[0])
                    self.agents[j].update_score(result[1])

    def print_results(self):
        self.agents.sort(key=lambda x: x.score, reverse=True)
        for i in range(self.agents_num):
            self.agents[i].print()


Simulation(100)
