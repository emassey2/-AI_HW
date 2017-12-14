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

    def check_vertically(self):
        #Check if the tokens appear four times in a vertical manner
        vertical_counter = 0
        winning_character = ' '
        for j in xrange(self.columns):
            for i in xrange(self.rows):
                if self.board[i][j] != ' ':
                    if winning_character != self.board[i][j]:
                        vertical_counter = 1
                        winning_character = self.board[i][j]
                    else:
                        vertical_counter += 1
                else:
                    vertical_counter = 0
                if vertical_counter >= self.goal_length:
                    if winning_character == self.player_1_token:
                        self.winner = "Player 1"
                    else:
                        self.winner = "Player 2"
                    print "The winner is ", self.winner
                    return True

            else:
                vertical_counter = 0
                # print "pos ", i,j
                # print "char ",winning_character
                # print "counter ", vertical_counter

        return False

    def check_horizontally(self):
        horizontal_counter = 0
        winning_character = ' '

        for i in xrange(self.rows):
            for j in xrange(self.columns):
                if self.board[i][j] != ' ':
                    if winning_character != self.board[i][j]:
                        horizontal_counter = 1
                        winning_character = self.board[i][j]
                    else:
                        horizontal_counter += 1
                else:
                    horizontal_counter = 0
                # print "pos ", i,j
                # print "cchar ", self.board[i][j]
                # print "wchar ",winning_character
                # print "counter ", horizontal_counter
                if horizontal_counter >= self.goal_length:
                    if winning_character == self.player_1_token:
                        self.winner = "Player 1"
                    else:
                        self.winner = "Player 2"
                    print "The winner is ", self.winner
                    return True

            else:
                horizontal_counter = 0
                # print "pos ", i,j
                # print "char ",winning_character
                # print "counter ", vertical_counter
        return False

    def check_diagonally(self):
        # TODO simplify and improved counting based off the min number of
        # tiles in a row (we can eliminate some early diags that have a length
        # less than goal tiles)
        horizontal_counter = 0
        winning_character = ' '

        # start in the lower right hand corner and count up and to the right
        for start_row in xrange(self.rows, 0, -1):
            for col in xrange(self.columns, 0, -1):
                row = self.rows - 1

                while (col < self.columns and row >= 0 ):

                    #print "pos ", row, col
                    #print "cchar ", self.board[row][col]
                    #print "wchar ", winning_character
                    #print "counter ", horizontal_counter

                    if self.board[row][col] != ' ':
                        if winning_character != self.board[row][col]:
                            horizontal_counter = 1
                            winning_character = self.board[row][col]
                        else:
                            horizontal_counter += 1
                    else:
                        horizontal_counter = 0

                    col += 1
                    row -= 1

                if horizontal_counter >= self.goal_length:
                    if winning_character == self.player_1_token:
                        self.winner = "Player 1"
                    else:
                        self.winner = "Player 2"
                    print "The winner is ", self.winner
                    return True

                horizontal_counter = 0


        # start in the lower left hand corner and count up and to the left
        for start_row in xrange(self.rows, 0, -1):
            for col in xrange(self.columns):
                row = self.rows - 1

                while (col >= 0 and row >= 0 ):

                    if self.board[row][col] != ' ':
                        if winning_character != self.board[row][col]:
                            horizontal_counter = 1
                            winning_character = self.board[row][col]
                        else:
                            horizontal_counter += 1
                    else:
                        horizontal_counter = 0
                        #print "pos ", row, col
                        #print "cchar ", self.board[row][col]
                        #print "wchar ",winning_character
                        #print "counter ", horizontal_counter

                    if horizontal_counter >= self.goal_length:
                        if winning_character == self.player_1_token:
                            self.winner = "Player 1"
                        else:
                            self.winner = "Player 2"
                        print "The winner is ", self.winner
                        return True

                    col -= 1
                    row -= 1

                horizontal_counter = 0


        return False



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
    finish = game.check_vertically()
    finish = game.check_horizontally()
    finish = game.check_diagonally()
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
