from random import randint
import math
from copy import deepcopy
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
DEPTH = 3
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.opponent = {1:2,2:1}
        self.color = 2
    def get_move(self,move):
        # opponents move
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
                               
        def minmax(color, depth, board):
            # if depth limit is reached then return the heurstic of percentage of black pieces over total pieces
            # check for win
            if board.is_win(color):
                if color == self.color:
                    return 1
                else:
                    return 0
            elif depth <= 0:
                return self.get_early_heuristic(board)
            moves = board.get_all_possible_moves(color)
            # init current max to infinity, negative if MAX player and positive if MIN player
            ma = math.inf
            if color == self.color:
                ma *= -1
            # iterate through all moves
            for index in range(len(moves)):
                for inner in range(len(moves[index])):
                    # MAX player
                    new_board = deepcopy(board)
                    if color == self.color:
                        new_board.make_move(moves[index][inner], color)
                        ma = max([minmax(self.opponent[color], depth -1, new_board)])
                    # MIN player
                    else:
                        new_board.make_move(moves[index][inner], color)
                        ma = min([minmax(self.opponent[color], depth -1, new_board)])
            return ma
        # initial pass through of all possible moves
        moves = self.board.get_all_possible_moves(self.color)
        output = open("debug.txt", 'a')
        for index in range(len(moves)):
            for inner in range(len(moves[index])):
                next_move = (max([minmax(self.opponent[self.color], DEPTH, self.board)]),moves[index][inner])
                output.write(str(next_move[0])+ ' ')
                output.write("\n")        

        output.write(f"final: {next_move[0]}\n")        
        self.board.make_move(next_move[1], self.color)
        return next_move[1]
        '''
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        self.board.make_move(move,self.color)
        return move
        ''' 
    def get_early_heuristic(self, board):
        black = 0
        white = 0
        for row in range(board.row):
            for col in range(board.col):
                piece = board.board[row][col]
                if piece.color == 'B':
                    if piece.is_king:
                        black += 1.2
                    else:
                        black += 1
                elif piece.color == 'W':
                    if piece.is_king:
                        white += 1.2
                    else:
                        white += 1
        return (black / (black + white)) if self.color == 1 else (white / (black+white))



