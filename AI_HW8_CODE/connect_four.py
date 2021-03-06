import sys
import copy
import math

MAX_DEPTH = 5
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

    def __init__(self, rows, columns, goal_length=4):

        self.rows = rows
        self.columns = columns
        self.winner = None
        self.goal_length = goal_length

    def create_board(self):
        #Create a 2D array of the size desired
        self.board = [[" " for i in range(self.columns)] for j in range(self.rows)]

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
                    if char == 'x':
                        outcome += self.player_2_token_colorized+'|'
                    elif char == 'o':
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
            # print "position ", i,column, self.board[i-1][column]
            if self.board[i-1][column] == ' ':
                self.board[i-1][column] = char
                valid = True
                break

        return valid

    # this check doubles as a heuristic
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

        token_won_v, token_score_v = self.check_vertically(token)
        token_won_h, token_score_h = self.check_horizontally(token)
        token_won_d, token_score_d = self.check_diagonally(token)
        #missing the diagonal
        total_score = token_score_v + token_score_h + token_score_d
        token_won = token_won_v or token_won_h or token_won_d

        return token_won, total_score

    def best_move(self, player_token):
        best_value = NEG_INF
        best_col = 0
        new_board = copy.deepcopy(self)
        for col in xrange(self.columns):
            valid = new_board.place_token(col, player_token)
            if valid:
                value = ab_min(new_board, player_token, NEG_INF, POS_INF, 1)
                print 'v  ', value
                print 'bv ', best_value
                if value > best_value:
                    best_value = value
                    best_col = col
            new_board = copy.deepcopy(self)

        return best_value, best_col

def ab_min(original_board, token, alpha, beta, depth = 0):
    won, score = original_board.goal_test(token)

    if depth >= MAX_DEPTH or won:
        score = math.ceil(float(score) / float(2**depth))
        if token == 'o':
            score = -score
        print 'min end ', score
        return score

    new_token = 'x' if token == 'o' else 'o'
    new_board = copy.deepcopy(original_board)

    for col in xrange(original_board.columns):
        valid = new_board.place_token(col, new_token)

        if valid:
            max_val = ab_max(new_board, new_token, alpha, beta, depth + 1)
            beta = min(beta, max_val)
            print token, 'score', score
            new_board.print_board()

        new_board = copy.deepcopy(original_board)

        if alpha >= beta:
            break #Cutting off the tree

    return beta


def ab_max(original_board, token, alpha, beta, depth = 0):
    won, score = original_board.goal_test(token)

    if depth >= MAX_DEPTH or won:
        score = math.ceil(float(score) / float(2**depth))
        if token == 'x':
            score = -score
        print 'max end ', score
        return score

    new_token = 'x' if token == 'o' else 'o'
    new_board = copy.deepcopy(original_board)

    for col in xrange(original_board.columns):
        valid = new_board.place_token(col, new_token)

        if valid:
            min_val = ab_min(new_board, new_token, alpha, beta, depth + 1)
            alpha = max(alpha, min_val)
            print token, 'score', score
            new_board.print_board()

        new_board = copy.deepcopy(original_board)

        if alpha <= beta:
            break #Cutting off the tree

    return alpha

# def minimax(original_board, max_player, depth = 8):
#     if depth == 0:
#         return cur_board, depth
#         #Return the board corresponding to the best movement
#
#     if max_player: #True Player 1
#         bestvalue = float("-inf")
#         new_board = copy.deepcopy(original_board)
#
#         for col in xrange(self.columns):
#
#             new_board.place_token(col,new_board.player_1_token)
#             value = max(value, minimax(new_board, False, depth - 1))
#             bestvalue = max(bestvalue,value)
#
#         return cur_board, depth #Not sure
#
#     else: #False Player 2
#         bestvalue = float("inf")
#
#         for col in xrange(self.columns):
#
#             cur_board.place_token(col,cur_board.player_2_token)
#             value = min(value, minimax(cur_board, True, depth - 1))
#             best = min(bestvalue,value)
#
#         return cur_board, depth #Not sure

def test(game):
    game.place_token(2,'x')
    game.place_token(2,'x')
    game.place_token(2,'x')
    #game.place_token(0,'o')

    #game.place_token(1,'x')
    #game.place_token(1,'o')
    #game.place_token(1,'o')

    #game.place_token(2,'o')

    #game.place_token(3,'x')
    #game.place_token(3,'x')
    #game.place_token(3,'x')
    #game.place_token(3,'o')

    #game.place_token(4,'o')
    #game.place_token(4,'x')
    #game.place_token(4,'x')
    #game.place_token(4,'x')
    #game.place_token(4,'o')

    #game.place_token(5,'o')

    finish = game.check_vertically('o')
    print finish
    finish = game.check_horizontally('o')
    print finish
    finish = game.check_diagonally('o')
    print finish
    game.print_board()


if __name__ == '__main__':
    #Obtain the values from the user
    #rows, columns = raw_input ("Enter the size of the board: (rows col): ").split()

    #Convert the string to int
    #rows = int(rows)
    #columns = int(columns)

    #Create the object from class Board
    rows = 6
    columns = 7
    game = Board(rows,columns)

    #Create the characters for the players
    game.create_characters()

    #Create the board
    game.create_board()
    game.print_board()
    test(game)

    gameover = False
    while not gameover:
        #player one
        print 'Player One!'
        # col = int(raw_input('Enter a colum to place a tile\n'))
        value, col = game.best_move('o')
        game.place_token(col, 'o')
        game.print_board()
        gameover, score = game.goal_test('o')
        print "o's score", score, '\n'

        if not gameover:
            #player two
            print 'Player two!'
            col = int(raw_input('Enter a colum to place a tile\n'))
            game.place_token(col, 'x')
            game.print_board()
            gameover, score = game.goal_test('x')
            print "x's score: ", score, '\n'

        print '\n\n\n\n\n'
        print '********************************************************************************'
        print '\n\n\n\n\n'


    #test(game)
    # matrix[5][3] = 'x'
    # matrix[5][6] = 'o'
    # print matrix
