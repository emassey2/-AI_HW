import sys
import copy
import math
import random
import os

MAX_DEPTH = 4
NEG_INF = float("-inf")
POS_INF = float("inf")

def hilite(string, status, bold):

    #Function to assign a color for the figures
    attr = []
    if status == 1:
        # green
        attr.append('32')
    else:
        # red
        attr.append('31')

    if bold:
        attr.append('1')

    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

class Board:

    def __init__(self, rows, columns, goal_length = 4):
        self.rows = rows
        self.columns = columns
        self.winner = None
        self.finish = None
        self.players = [None, None]
        self.board = None
        self.goal_length = goal_length

    def create_board(self):
        #Create a 2D array of the size desired
        self.board = \
            [[" " for i in range(self.columns)] for j in range(self.rows)]

    def create_characters(self):
        #Set the desired color of the character defined
        self.player_1_token = 'o'
        self.player_2_token = 'x'
        self.player_1_token_colorized = hilite(self.player_1_token, 1, 1)
        self.player_2_token_colorized = hilite(self.player_2_token, 0, 1)

    def print_board(self):
        outcome = '|'
        divider = ''
        for i in xrange(rows+1):
            for j in xrange(columns):
                # print i,j

                #Last row to indicate the number of columns
                if i == rows:
                    outcome += str(j)+'|'
                else:

                    #Identify if there's a character already
                    char = self.board[i][j]
                    if char == self.player_2_token:
                        outcome += self.player_2_token_colorized+'|'
                    elif char == self.player_1_token:
                        outcome += self.player_1_token_colorized+'|'
                    else:
                        outcome += char+'|'
                    divider += '=='
            print outcome
            print divider
            outcome = '|'
            divider = ''

    def place_token(self,column,char):
        valid = False
        #Place a token in the desired location
        for i in xrange(self.rows, 0, -1):
            if self.board[i-1][column] == ' ':
                self.board[i-1][column] = char
                valid = True
                #Once we place a token we break the loop
                break

        return valid

    def check_vertically(self, token):
        #Check if the tokens appear four times in a vertical manner
        token_counter = 0
        token_won = False
        token_score = 0

        for j in xrange(self.columns):
            for i in xrange(self.rows):

                # if we have seen another one of our tokens, increment our count
                if self.board[i][j] == token:
                    token_counter += 1

                # this isn't our token. add to our score and reset our count
                else:
                    token_score += token_counter**2
                    token_counter = 0

                # check if we have won
                if token_counter >= self.goal_length:
                    token_won = True
                    token_score = sys.maxint

                    if token_won:
                        break

            if token_won:
                break
            else:
                # switching to the next column so we need to update our count/score
                token_score += token_counter**2
                token_counter = 0

        return token_won, token_score


    # this check doubles as a heuristic
    def check_horizontally(self, token):
        #Check if the tokens appear four times in a horizontal manner
        token_counter = 0
        token_won = False
        token_score = 0

        for i in xrange(self.rows):
            for j in xrange(self.columns):

                # if we have seen another one of our tokens, increment our count
                if self.board[i][j] == token:
                    token_counter += 1

                # this isn't our token. add to our score and reset our count
                else:
                    token_score += token_counter**2
                    token_counter = 0

                # check if we have won
                if token_counter >= self.goal_length:
                    token_won = True
                    token_score = sys.maxint

                    if token_won:
                        break

            if token_won:
                break
            else:
                # switching to the next column so we need to update our count/score
                token_score += token_counter**2
                token_counter = 0

        return token_won, token_score


    def check_diagonally(self, token):
        token_counter = 0
        token_won = False
        token_score = 0

        # explore up and to the right, move along the bottom row
        for starting_col in xrange(self.columns - (self.goal_length), -1, -1):
            row = self.rows - 1
            col = starting_col
            while (col < self.columns and row >= 0 ):

                # if we have seen another one of our tokens, increment our count
                if self.board[row][col] == token:
                    token_counter += 1

                # this isn't our token. add to our score and reset our count
                else:
                    token_score += token_counter**2
                    token_counter = 0

                # if we have won we are done
                if token_counter >= self.goal_length:
                    token_won = True
                    return token_won, token_score

                col += 1
                row -= 1

            # switching to the next diag so we need to update our count/score
            token_score += token_counter**2
            token_counter = 0

        # explore up and to the right, move up the left most column
        for starting_row in xrange(self.rows-1, self.rows - (self.goal_length), -1):
            row = starting_row
            col = 0

            while (col < self.columns and row >= 0 ):

                # if we have seen another one of our tokens, increment our count
                if self.board[row][col] == token:
                    token_counter += 1

                # this isn't our token. add to our score and reset our count
                else:
                    token_score += token_counter**2
                    token_counter = 0

                # if we have won we are done
                if token_counter >= self.goal_length:
                    token_won = True
                    return token_won, token_score

                col += 1
                row -= 1

            # switching to the next diag so we need to update our count/score
            token_score += token_counter**2
            token_counter = 0


        # explore up and to the left, move along the bottom row
        for starting_col in xrange(self.goal_length-1, self.columns):
            row = self.rows - 1
            col = starting_col

            while (col >=0 and row >= 0 ):

                # if we have seen another one of our tokens, increment our count
                if self.board[row][col] == token:
                    token_counter += 1

                # this isn't our token. add to our score and reset our count
                else:
                    token_score += token_counter**2
                    token_counter = 0

                # if we have won we are done
                if token_counter >= self.goal_length:
                    token_won = True
                    return token_won, token_score

                col -= 1
                row -= 1

            # switching to the next diag so we need to update our count/score
            token_score += token_counter**2
            token_counter = 0

        # explore up and to the left, move up the right most column
        for starting_row in xrange(self.rows-1, self.rows - (self.goal_length), -1):
            row = starting_row
            col = self.columns - 1

            while (col >= 0 and row >= 0 ):

                # if we have seen another one of our tokens, increment our count
                if self.board[row][col] == token:
                    token_counter += 1

                # this isn't our token. add to our score and reset our count
                else:
                    token_score += token_counter**2
                    token_counter = 0

                # if we have won we are done
                if token_counter >= self.goal_length:
                    token_won = True
                    return token_won, token_score

                col -= 1
                row -= 1

            # switching to the next diag so we need to update our count/score
            token_score += token_counter**2
            token_counter = 0

        return token_won, token_score

    def goal_test(self, token):
        #Collect the test results of the desired player
        token_won_v, token_score_v = self.check_vertically(token)
        token_won_h, token_score_h = self.check_horizontally(token)
        token_won_d, token_score_d = self.check_diagonally(token)

        #Perform a test for the opponent
        if token == self.player_1_token:
            op_token = self.player_2_token
        else:
            op_token = self.player_1_token

        #Collect the test results of the opponent
        _, op_token_score_v = self.check_vertically(op_token)
        _, op_token_score_h = self.check_horizontally(op_token)
        _, op_token_score_d = self.check_diagonally(op_token)

        #Combine both results

        total_score = (token_score_v - op_token_score_v) + \
                      (token_score_h - op_token_score_h) + \
                      (token_score_d - op_token_score_d)

        #Set a winner flag in case that the player won with that movement
        token_won = token_won_v or token_won_h or token_won_d

        return token_won, total_score

    def best_move(self, player_token,algorithm):
        best_value = NEG_INF
        best_col = 0
        #Back up of the board
        new_board = copy.deepcopy(self)

        for col in xrange(self.columns):
            #Evaluate placing a token in every column and use the best one
            valid = new_board.place_token(col, player_token)

            #Only evaluate valid placements
            if valid:
                #Evaluate the min using the selected algorithm
                if algorithm == 'ab':
                    value = ab_min(new_board, player_token, NEG_INF, POS_INF, 1)
                else:
                    value = minm(new_board, player_token, 1)

                if value > best_value:
                    best_value = value
                    best_col = col

            #Revert changes
            new_board = copy.deepcopy(self)

        return best_value, best_col

def minm(original_board, token, depth = 0):
    #Goal test
    won, score = original_board.goal_test(token)

    #In case we reached the max depth or player won
    if depth >= MAX_DEPTH or won:
        #Penalize based on the depth
        score = math.ceil(float(score) / float(2**depth))

        if token == original_board.player_1_token:
            score = -score
        return score

    #Change the token for the max turn
    new_token = original_board.player_2_token \
        if token == original_board.player_1_token else original_board.player_1_token

    #Create a backup of the board
    new_board = copy.deepcopy(original_board)

    value = POS_INF

    #Create a list of possible positions for the token
    token_positions = list(range(0,new_board.columns))

    #Random shuffle to get a better evaluation
    random.shuffle(token_positions)

    for col in xrange(original_board.columns):
        #Place the token in the desired location
        valid = new_board.place_token(token_positions[col], new_token)

        #If it was a valid placement
        if valid:
            #Get the max value of the upcoming movements
            max_val = maxm(new_board, new_token, depth + 1)

            #Get the min between the current value and the max_val
            value = min(value, max_val)

        #Restore the board
        new_board = copy.deepcopy(original_board)

    return value

def ab_min(original_board, token, alpha, beta, depth = 0):
    #Goal test
    won, score = original_board.goal_test(token)

    #In case we reached the max depth or player won
    if depth >= MAX_DEPTH or won:
        #Penalize based on the depth
        score = math.ceil(float(score) / float(2**depth))
        if token == original_board.player_1_token:
            score = -score
        return score

    #Change the token for the max turn
    new_token = original_board.player_2_token \
        if token == original_board.player_1_token else original_board.player_1_token

    #Create a backup of the board
    new_board = copy.deepcopy(original_board)

    value = POS_INF

    #Create a list of possible positions for the token
    token_positions = list(range(0,new_board.columns))

    #Random shuffle to get a better evaluation
    random.shuffle(token_positions)

    for col in xrange(original_board.columns):
        #Place the token in the desired location
        valid = new_board.place_token(token_positions[col], new_token)

        if valid:
            #Get the max value of the upcoming movements
            max_val = ab_max(new_board, new_token, alpha, beta, depth + 1)

            #Get the min between the current value and the max_val
            value = min(value, max_val)

        #Restore the board
        new_board = copy.deepcopy(original_board)

        #Evaluate prunning condition
        if value <= alpha:
            #Chomp the tree
            break

        beta = min(beta, value)

    return value

def maxm(original_board, token, depth = 0):
    #Goal test
    won, score = original_board.goal_test(token)

    #In case we reached the max depth or player won
    if depth >= MAX_DEPTH or won:
        #Penalize based on the depth
        score = math.ceil(float(score) / float(2**depth))
        if token == original_board.player_2_token:
            score = -score
        return score

    #Change the token for the min turn
    new_token = original_board.player_2_token \
        if token == original_board.player_1_token else original_board.player_1_token

    #Create a backup of the board
    new_board = copy.deepcopy(original_board)

    value = NEG_INF

    #Create a list of possible positions for the token
    token_positions = list(range(0,new_board.columns))

    #Random shuffle to get a better evaluation
    random.shuffle(token_positions)

    for col in xrange(original_board.columns):
        #Place the token in the desired location
        valid = new_board.place_token(token_positions[col], new_token)

        if valid:
            #Get the min value of the upcoming movements
            min_val = minm(new_board, new_token, depth + 1)

            #Get the max between the current value and the min_val
            value = max(value, min_val)

        #Restore the board
        new_board = copy.deepcopy(original_board)

    return value

def ab_max(original_board, token, alpha, beta, depth = 0):
    #Goal test
    won, score = original_board.goal_test(token)

    #In case we reached the max depth or player won
    if depth >= MAX_DEPTH or won:
        score = math.ceil(float(score) / float(2**depth))
        if token == original_board.player_2_token:
            score = -score
        return score

    #Change the token for the min turn
    new_token = original_board.player_2_token \
        if token == original_board.player_1_token else original_board.player_1_token

    #Create a backup of the board
    new_board = copy.deepcopy(original_board)

    value = NEG_INF

    #Create a list of possible positions for the token
    token_positions = list(range(0,new_board.columns))

    #Random shuffle to get a better evaluation
    random.shuffle(token_positions)
    for col in xrange(original_board.columns):
        #Place the token in the desired location
        valid = new_board.place_token(token_positions[col], new_token)

        if valid:
            #Get the min value of the upcoming movements
            min_val = ab_min(new_board, new_token, alpha, beta, depth + 1)

            #Get the max between the current value and the min_val
            value = max(value, min_val)

        #Restore the board
        new_board = copy.deepcopy(original_board)

        #Evaluate prunning condition
        if value >= beta:
            #Chomp the tree
            break

        alpha = max(alpha, value)

    return value

if __name__ == '__main__':
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
    print "---------- Connect 4 ----------"
    rows, columns = raw_input \
        ("Select the size of the board: (rows col): ").split()

    # Convert the string to int
    rows = int(rows)
    columns = int(columns)

    #Create the object from class Board
    # rows = 6
    # columns = 7
    game = Board(rows,columns)

    #Create the characters for the players
    game.create_characters()

    #Create the board
    game.create_board()
    game.print_board()

    game.players[0] = \
        raw_input("Select the type for player 1 (h -> Human, m -> machine ): ")

    game.players[1] = \
        raw_input("Select the type for player 2 (h = Human, m = machine ): ")

    if game.players[1] == 'm' or game.players[0] == 'm' :
        MAX_DEPTH = int(raw_input("Select difficulty level (2 - 8): "))
        algorithm = \
            raw_input("Select ab for alpha-beta algorithm or mi for just minimax ")



    gameover = False
    while not gameover:
        #player one 'o'
        if game.players[0] == 'h':
            print 'Player One as a Human'
            col = int(raw_input('Enter a colum to place a tile\n'))
            if col >= game.columns:
                print "Invalid option "
                col = int(raw_input('Enter a colum to place a tile\n'))
        else:
            print 'Player One as a Machine'
            value, col = game.best_move(game.player_1_token,algorithm)
        game.place_token(col, game.player_1_token)
        game.print_board()
        gameover, score = game.goal_test(game.player_1_token)
        print "o's score", score, '\n'
        #
        if not gameover:
            #player two 'x'
            if game.players[1] == 'h':
                print 'Player two as a Human'
                col = int(raw_input('Enter a colum to place a tile\n'))
                if col >= game.columns:
                    print "Invalid option "
                    col = int(raw_input('Enter a colum to place a tile\n'))
            else:
                print 'Player two as a Machine'
                value, col = game.best_move(game.player_2_token,algorithm)
            game.place_token(col, game.player_2_token)
            game.print_board()
            gameover, score = game.goal_test(game.player_2_token)
            print "x's score: ", score, '\n'
        print '\n\n\n\n\n'
        print '********************************************************************************'
        print '\n\n\n\n\n'
