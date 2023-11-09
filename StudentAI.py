from random import randint
import math
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    def get_move(self,move):
        # opponents move
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
                               
        def minmax(move, color, depth):
            # if depth limit is reached then return the heurstic of percentage of black pieces over total pieces
            if depth <= 0:
                return self.board.black_count / (self.board.black_count + self.board.white_count)
            # make previous turns move here
            if len(move) != 0:
                self.board.make_move(move, self.opponent[color])
            else:
                color = self.opponent[color]
            # check for win here return 0 if white wins 1 if black wins
            if self.board.is_win(self.opponent[color]):
                return 0 if self.opponent[color] == 1 else 1
            
            moves = self.board.get_all_possible_moves(color)
            # init current max to infinity, negative if MAX player and positive if MIN player
            ma = math.inf
            if color == self.color:
                ma *= -1
            # iterate through all moves
            for index in range(len(moves)):
                for inner in range(len(moves[index])):
                    # MAX player
                    if color == self.color:
                        ma = max([minmax(moves[index][inner], self.opponent[color], depth -1)])
                    # MIN player
                    else:
                        ma = min([minmax(moves[index][inner], self.opponent[color], depth -1)])
                    # if depth is 1 then the last move did not actually make a move so we only undo if depth is > 1.
                    if depth > 1:
                        self.board.undo()
            return ma
        # initial pass through of all possible moves
        moves = self.board.get_all_possible_moves(self.color)
        for index in range(len(moves)):
            for inner in range(len(moves[index])):
                next_move = max([(minmax(moves[index][inner],self.opponent[self.color], 3),moves[index][inner])], key = lambda x : x[0])
                self.board.undo()
        self.board.make_move(next_move[1],self.color)
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
        

