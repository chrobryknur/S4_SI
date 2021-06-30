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

    def __init__(self, pawn, knight, bishop, rook, queen):
        self.PAWN = pawn
        self.KNIGHT = knight
        self.BISHOP = bishop
        self.ROOK = rook
        self.QUEEN = queen

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

    def __init__(self, pawn, knight, bishop, rook, queen, alpha):
        self.weights = Weights(pawn, knight, bishop, rook, queen)
        self.alpha = alpha
        self.scores = None

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
        print("Agent ")
        print("Scores against best agents: " + str(self.scores))
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
    def __init__(self, games_num, generated_agents_num, generations):
        self.best_agents = [
            Agent(1, 0, 9, 3, 10, 0.10799009802120252),
            Agent(1, 8, 4, 5, 4,  0.1920717303053845),
            Agent(1, 5, 6, 2, 8,  0.05320731652070465),
            Agent(1, 5, 4, 7, 7,  0.020787815382636077),
            Agent(1, 8, 3, 7, 6,  0.025238235260147346)
        ]
        self.games_num = games_num
        self.generated_agents_num = generated_agents_num
        self.generations = generations
        self.find_best_agent(self.generations)

    def play_vs_agent(self, agent):
        score = 0
        won = 0
        drawn = 0
        lost = 0
        for i in range(5):
            for j in range(self.games_num):
                G = None
                if random.random() < 0.5:
                    G = Game(agent, self.best_agents[i])
                    result = G.play()
                    score += result[0]
                    if result[0] == 1:
                        won += 1
                    elif result[0] == 0.5:
                        drawn += 1
                    else:
                        lost += 1

                else:
                    G = Game(self.best_agents[i], agent)
                    result = G.play()
                    score += result[1]
                    if result[1] == 1:
                        won += 1
                    elif result[1] == 0.5:
                        drawn += 1
                    else:
                        lost += 1
        print(score)
        print(won)
        print(drawn)
        print(lost)

    def best_agent(self):
        scores = [0, 0, 0, 0, 0]
        for i in range(5):
            for j in range(5):
                if i != j:
                    for k in range(self.games_num):
                        G = Game(self.best_agents[i], self.best_agents[j])
                        result = G.play()
                        scores[i] += result[0]
                        scores[j] += result[1]
        maximum_score = 0
        best_agent = None
        for i in range(5):
            if scores[i] > maximum_score:
                maximum_score = scores[i]
                best_agent = self.best_agents[i]
        print("Best agent")
        best_agent.print()
        return

    def small_diff(self):
        diff = random.random()
        if random.random() < 0.5:
            diff *= -1
        return diff

    def find_best_agent(self, depth):
        if depth == 0:
            return self.best_agent()

        alpha_sorted = sorted(self.best_agents, key=lambda x: x.alpha)
        alpha_range = [alpha_sorted[0].alpha, alpha_sorted[-1].alpha]

        knight_mean = sum(x.weights.KNIGHT for x in self.best_agents)/5
        bishop_mean = sum(x.weights.BISHOP for x in self.best_agents)/5
        rook_mean = sum(x.weights.ROOK for x in self.best_agents)/5
        queen_mean = sum(x.weights.QUEEN for x in self.best_agents)/5

        queue = PriorityQueue()
        unique = count()

        for i in range(self.generated_agents_num):
            knight_weight = knight_mean + self.small_diff()
            bishop_weight = bishop_mean + self.small_diff()
            rook_weight = rook_mean + self.small_diff()
            queen_weight = queen_mean + self.small_diff()

            alpha = random.random()
            while alpha < alpha_range[0] or alpha > alpha_range[1]:
                alpha = random.random()

            new_agent = Agent(1, knight_weight, bishop_weight,
                              rook_weight, queen_weight, alpha)
            scores = []
            for j in range(5):
                score = 0
                for k in range(self.games_num):
                    if random.randint(0, 9) % 2:
                        G = Game(new_agent, self.best_agents[j])
                        result = G.play()
                        score += result[0]
                    else:
                        G = Game(self.best_agents[j], new_agent)
                        result = G.play()
                        score += result[1]
                scores.append(score)
            new_agent.scores = scores
            queue.put((-sum(scores), next(unique), new_agent))

        result = queue.get()
        agent = result[2]
        maximum_score = 0
        worst_agent = None
        for i in range(5):
            if agent.scores[i] >= maximum_score:
                maximum_score = agent.scores[i]
                worst_agent = i
        if maximum_score > 0.5 * self.games_num:
            print("Swapping agent")
            self.best_agents[worst_agent].print()
            self.best_agents[worst_agent] = agent
            print("with agent")
            agent.print()

        self.find_best_agent(depth - 1)


Simulation(20, 20, 20)
