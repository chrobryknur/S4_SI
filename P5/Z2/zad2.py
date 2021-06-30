#!/usr/bin/python3

from os import read
import random
import chess
import chess.polyglot
import chess.syzygy


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

reader = chess.polyglot.open_reader("data.bin") # https://chess.massimilianogoi.com/download/database/gamesarchive/ converted to bin using polyglot
tablebase = chess.syzygy.open_tablebase("./syzygy") # sygyzy ending table

class Game:
    def __init__(self):
        self.board = chess.Board()
        self.moves_cnt = 0

    def do_move(self, move):
        self.board.push(move)

    def result(self):
        if self.board.outcome().winner == chess.WHITE:
            return 100 - self.moves_cnt
        if self.board.outcome().winner == chess.BLACK:
            return -1000
        return -100

    def terminal(self):
        return bool(self.board.outcome())

    def random_move(self):
        ms = list(self.board.legal_moves)
        move = random.choice(ms)
        return move

    def evaluate_board(self, moves_num):

        if self.board.is_checkmate():
            if self.board.turn:
                return 9999999
            return -9999999

        if self.board.is_stalemate():
            if self.board.turn:
                return -100000
            return 100000

        wdl = tablebase.get_wdl(self.board)

        if wdl:
            if wdl == 0:
                if self.board.turn:
                    return -10000
                return 10000

            if self.board.turn and wdl > 0:
                return 999999
            elif self.board.turn and wdl < 0:
                return -999999
            elif not self.board.turn and wdl > 0:
                return -999999
            else:
                return 999999
         

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
        
        eval += 0.1 * (moves_num - len(list(self.board.legal_moves)))

        if self.board.turn: # black has moved so now it will be white's turn
            return -eval    # but evaluating for black so return -eval
        return eval

    def minimax(self, depth, is_white):
        best_move_value = -99999999
        best_move = None

        possible_moves_num = len(list(self.board.legal_moves))
        for move in list(self.board.legal_moves):
            self.board.push(move)
            value = self.alpha_beta(depth - 1, -10000000, 10000000, not is_white, possible_moves_num)
            self.board.pop()
            if value >= best_move_value:
                best_move_value = value
                best_move = move

        return best_move


    def alpha_beta(self, depth, alpha, beta, is_white, moves_num):
        if not depth or self.board.outcome():
            return -self.evaluate_board(moves_num)

        possible_moves_num = len(list(self.board.legal_moves))
        if is_white:
            best_move = -99999999
            for move in list(self.board.legal_moves):
                self.board.push(move)
                best_move = max(best_move, self.alpha_beta(depth-1, alpha, beta, not is_white, possible_moves_num))
                self.board.pop()
                alpha = max(alpha, best_move)
                if beta <= alpha:
                    return best_move
            return best_move

        else:
            best_move = 99999999
            for move in list(self.board.legal_moves):
                self.board.push(move)
                best_move = min(best_move, self.alpha_beta(depth-1, alpha, beta, not is_white, possible_moves_num))
                self.board.pop()
                beta = min(beta, best_move)
                if beta <= alpha:
                    return best_move
            return best_move

    def best_move(self):
        possible_move = reader.get(self.board)
        if possible_move:
            return possible_move.move
        depth = 2 # something is wrong with uneven depth values
        return self.minimax(depth, self.board.turn) 

    def agent_move(self):
        self.moves_cnt+=1
        return self.best_move()

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
            print(G.result())
            print(G.board.fen())
            break
    result += G.result()

print(result/games)

def proof_of_concept():
    board = chess.Board("8/2K5/4B3/3N4/8/8/4k3/8 w - - 0 1")
    wdl = tablebase.get_wdl(board)

    if wdl:
        if wdl == 0:
            if board.turn:
                return -10000
            return 10000

        if board.turn and wdl > 0:
            return 999999
        elif board.turn and wdl < 0:
            return -999999
        elif not board.turn and wdl > 0:
            return -999999
        else:
            return 999999

# print(proof_of_concept())
