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
            # make previous turns move here
            self.board.make_move(move, self.opponent[color])

            # if depth limit is reached then return the heurstic of percentage of black pieces over total pieces
            if depth <= 0:
                return self.get_early_heuristic(self.board, self.color)

            # check for win here return 0 if white wins 1 if black wins
            if self.board.is_win(self.opponent[color]):
                if self.opponent[color] == self.color:
                    return 1
                else:
                    return 0
            
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
                        ma = max(ma, minmax(moves[index][inner], self.opponent[color], depth -1))
                    # MIN player
                    else:
                        ma = min(ma, minmax(moves[index][inner], self.opponent[color], depth -1))
                    self.board.undo()
            return ma
        
        #method = "minimax"
        method = "mcts"

        if method == "minimax":
            # initial pass through of all possible moves
            moves = self.board.get_all_possible_moves(self.color)
            #output = open("debug.txt", 'a')
            next_move = (-math.inf, '')
            for index in range(len(moves)):
                for inner in range(len(moves[index])):
                    next_move = max(next_move, (minmax(moves[index][inner],self.opponent[self.color], DEPTH),moves[index][inner]), key = lambda x: x[0])
                    self.board.undo()
                    #output.write(str(next_move[0])+ ' ')
                #output.write("\n")        
            self.board.make_move(next_move[1],self.color)
            #output.write(f"final: {next_move[0]}\n")
            return next_move[1]
        elif method == "mcts":
            def simulate(board):
                """
                Simulates a single game from the current state and returns the winner. Logic taken from GameLogic.py
                Return values:
                -1 = Tie
                1 = player 1 wins (black)
                2 = player 2 wins (white)
                """
                player = 2 # Initial move made by black, white's turn now
                winPlayer = 0
                sim_move = Move([])
                while True:
                    sim_move = get_random_move(player, board)
                    if sim_move == None:
                        # Current player just lost
                        return 2 if player == 1 else 1
                    board.make_move(sim_move, player)
                    winPlayer = board.is_win(player)
                    if winPlayer != 0:
                        break
                    if player == 1:
                        player = 2
                    else:
                        player = 1
                return winPlayer

            def get_random_move(color, board):
                # From base code, get a random move

                moves = board.get_all_possible_moves(color)
                # Check for empty list
                if len(moves) == 0:
                    return None

                index = randint(0,len(moves)-1)
                inner_index =  randint(0,len(moves[index])-1)
                move = moves[index][inner_index]
                #self.board.make_move(move,self.color)
                return move

            output = open("debug.txt", 'a')

            # For each move, keep track of number of games simulated with that move along with how many wins
            moves = self.board.get_all_possible_moves(self.color)
            simulate_cnt = {}
            win_cnt = {}
            for index in range(len(moves)):
                for inner in range(len(moves[index])):
                    curr_move = moves[index][inner]
                    simulate_cnt[str(curr_move)] = 0
                    win_cnt[str(curr_move)] = 0

            # Simulation loop
            simulate_total = 1000 # Total number of simulations to be ran (this can be changed to be time based)
            for i in range(simulate_total):
                move_init = get_random_move(self.color, self.board)
                simulate_cnt[str(move_init)] += 1
                self.board.make_move(move_init, self.color)
                board_copy = deepcopy(self.board)
                winner = simulate(board_copy)
                if winner == 1 or winner == -1:
                    win_cnt[str(move_init)] += 1
                self.board.undo()

            # Get move with best winrate
            best_move = (Move([]), -1)
            for index in range(len(moves)):
                for inner in range(len(moves[index])):
                    curr_move = moves[index][inner]
                    if simulate_cnt[str(curr_move)] == 0:
                        continue
                    wr = win_cnt[str(curr_move)] / simulate_cnt[str(curr_move)]
                    if wr > best_move[1]:
                        best_move = (curr_move, -1)

            self.board.make_move(best_move[0], self.color)
            return best_move[0]

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
    def get_early_heuristic(self, board, turn):
        black = 0
        white = 0
        for row in range(board.row):
            for col in range(board.col):
                piece = board.board[row][col]
                if piece.color == 'B':
                    if piece.is_king:
                        black += 1.5
                    else:
                        black += 1
                    if piece.row == 0 or piece.row == (board.row - 1) or piece.col == 0 or piece.col == (board.col - 1):
                        black += 0.2
                elif piece.color == 'W':
                    if piece.is_king:
                        white += 1.5
                    else:
                        white += 1
                    if piece.row == 0 or piece.row == (board.row - 1) or piece.col == 0 or piece.col == (board.col - 1):
                        white += 0.2
        return black / (black + white) if turn == 1 else white / (black+white)



