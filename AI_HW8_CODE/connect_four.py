import sys

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
        #Place a token in the desired location
        for i in xrange(self.rows, 0, -1):
            # print "position ", i,column, self.board[i-1][column]
            if self.board[i-1][column] == ' ':
                self.board[i-1][column] = char
                break

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

    def goal_test(self,token):

        token_won_v, token_score_v = self.check_vertically(token)
        token_won_h, token_score_h = self.check_horizontally(token)
        token_won_d, token_score_d = self.check_diagonally(token)
        #missing the diagonal
        total_score = token_score_v + token_score_h + token_score_d
        token_won = token_won_v or token_won_h or token_won_d

        return player_won, total_score

def alphabeta_minimax(original_board, max_player, alpha, beta, depth = 8):

    if max_player: #True Player 1
        p_1_won,
        if depth == 0:
            return cur_board, depth
            #Return the board corresponding to the best movement

        value = float("-inf")
        new_board = copy.deepcopy(original_board)

        for col in xrange(self.columns):

            new_board.place_token(col,new_board.player_1_token)
            value = max(value, alphabeta_minimax(new_board, False, alpha, beta, depth - 1))
            alpha = max(alpha,value)

            if beta <= alpha:
                break #Cutting off the tree

        return cur_board, depth #Not sure

    else: #False Player 2
        value = float("inf")

        for col in xrange(self.columns):

            cur_board.place_token(col,cur_board.player_2_token)
            value = min(value, alphabeta_minimax(cur_board, True, alpha, beta, depth - 1))
            alpha = min(beta,value)

            if beta <= alpha:
                break #Cutting off the tree

        return cur_board, depth #Not sure

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
    game.place_token(1,'x')
    game.place_token(2,'x')
    game.place_token(3,'x')
    game.place_token(4,'x')
    game.place_token(5,'o')
    game.place_token(2,'o')
    game.place_token(5,'o')
    game.place_token(2,'o')
    game.place_token(5,'o')
    game.place_token(2,'o')
    game.place_token(5,'o')
    game.place_token(2,'x')
    game.place_token(2,'o')

    game.place_token(3,'o')
    game.place_token(4,'o')
    game.place_token(4,'o')
    game.place_token(5,'o')
    game.place_token(6,'o')
    game.place_token(6,'o')
    game.place_token(6,'o')
    game.place_token(6,'o')
    game.place_token(6,'o')
    game.place_token(6,'o')
    finish = game.check_vertically('o')
    finish = game.check_horizontally('o')
    finish = game.check_diagonally('o')
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
    # matrix[5][3] = 'x'
    # matrix[5][6] = 'o'
    # print matrix
