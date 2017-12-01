#!/usr/bin/python


from itertools import islice
import copy
import sys
from sets import Set
import time


DEBUG_LEVEL = 0
PRINT_STATEMENTS = False


class Sudoku:
    SUDOKU_SIDE_LENGTH = 9
    SUDOKU_SUB_SIZE = 3
    SUDOKU_SET = set({'1', '2', '3', '4', '5', '6', '7', '8', '9'})

    # state is a 9x9 array of number in range [0,9]
    def __init__(self, state):
        self.state = state
        self.domain_space = self.get_all_domain_space()


    def get_all_domain_space(self):
        domain_space = [[None for x in xrange(self.SUDOKU_SIDE_LENGTH)] \
                              for y in xrange(self.SUDOKU_SIDE_LENGTH)]

        for i in xrange(0, self.SUDOKU_SIDE_LENGTH):
            for j in xrange(0, self.SUDOKU_SIDE_LENGTH):
                valid_set = self.get_super_set(i, j)

                # find the difference between all possible numbers and our superset of
                # currently present numbers
                valid_set = self.SUDOKU_SET.difference(valid_set)
                domain_space[i][j] = valid_set


        if PRINT_STATEMENTS:
            print domain_space
        return domain_space

    def fill_in_tile(self, row, col, value):
        valid = True
        #Back up of our previous state
        old_state = copy.deepcopy(self.state)

        #Update the value in the current cell
        self.state[row][col] = value

        #Update the domain of the cells in the corresponding row
        for j in xrange(0, self.SUDOKU_SIDE_LENGTH):
            if self.state[row][j] == '0':
                valid_set = self.get_super_set(row, j)
                valid_set = self.SUDOKU_SET.difference(valid_set)
                if len(valid_set) != 0:
                    self.domain_space[row][j] = valid_set
                else:
                    valid = False

        #Update the domain of the cells in the corresponding column
        for i in xrange(0, self.SUDOKU_SIDE_LENGTH):
            if self.state[i][col] == '0':
                valid_set = self.get_super_set(i, col)
                valid_set = self.SUDOKU_SET.difference(valid_set)
                if len(valid_set) != 0:
                    self.domain_space[i][col] = valid_set
                else:
                    valid = False

        #Update the domain of the cells in the corresponding sub_square
        #Cells shared between the column, row, and sub_square updating part
        #are getting reupdated, that could be improved
        col_start = col/self.SUDOKU_SUB_SIZE
        row_start = row/self.SUDOKU_SUB_SIZE
        for i in xrange(col_start, col_start + self.SUDOKU_SUB_SIZE):
            for j in xrange(row_start, row_start + self.SUDOKU_SUB_SIZE):
                if self.state[i][j] == '0':
                    valid_set = self.get_super_set(i, j)
                    valid_set = self.SUDOKU_SET.difference(valid_set)
                    if len(valid_set) != 0:
                        self.domain_space[i][j] = valid_set
                    else:
                        False

        if not valid:
            self.state = copy.deepcopy(old_state)

        return valid

    def fill_in_tile_blind(self, row, col, value):
        #Update the value in the current cell
        self.state[row][col] = value

        return True


    @classmethod
    def str_to_sudoku_array(self, state_str):
        sudoku_array = []
        for i in xrange(0, self.SUDOKU_SIDE_LENGTH):
            sudoku_array.append([])
            for j in xrange(0, self.SUDOKU_SIDE_LENGTH):
                sudoku_array[i].append(state_str[i*self.SUDOKU_SIDE_LENGTH+j])

        return sudoku_array


    @classmethod
    def sudoku_array_to_str(self, sudoku_array):
        state_str = "\n"
        horizontal_bar = '\n------|-------|------\n'
        for i in xrange(0, self.SUDOKU_SUB_SIZE):
            for j in xrange(0, self.SUDOKU_SUB_SIZE):
                for k in xrange(0, self.SUDOKU_SUB_SIZE):
                    for l in xrange(0, self.SUDOKU_SUB_SIZE):
                        state_str += str(sudoku_array[j + i*self.SUDOKU_SUB_SIZE]\
                                                     [l + k*self.SUDOKU_SUB_SIZE])
                        state_str += ' '
                    state_str += '| '
                state_str = state_str[:-2] + '\n'
            state_str = state_str[:-1]
            state_str += horizontal_bar
        state_str = state_str[:-len(horizontal_bar)]

        return state_str
    @classmethod
    def sudoku_array_to_str_file(self, sudoku_array):
        state_str = ''
        for i in xrange(0, self.SUDOKU_SUB_SIZE):
            for j in xrange(0, self.SUDOKU_SUB_SIZE):
                for k in xrange(0, self.SUDOKU_SUB_SIZE):
                    for l in xrange(0, self.SUDOKU_SUB_SIZE):
                        state_str += str(sudoku_array[j + i*self.SUDOKU_SUB_SIZE]\
                                                     [l + k*self.SUDOKU_SUB_SIZE])
                state_str += '\n'
        return state_str


    def get_row_set(self,row_number):
        row = list()
        #Returns a set of all the current elements in a row
        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print "Checking row..."

        # find every number in our row
        for col in xrange(0, self.SUDOKU_SIDE_LENGTH):
            row.append(self.state[row_number][col])

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print row

        # convert that row to a set for easy comparison
        row_set = set(row)

        return row_set


    def get_column_set(self,column_number):
        #Returns a set of all the current elements in a column
        column = list()

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print "Checking col..."

        # find every number in our column
        for row in xrange(0, self.SUDOKU_SIDE_LENGTH):
            column.append(self.state[row][column_number])

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print column

        # convert that column to a set for easy comparison
        column_set = set(column)

        # if our column doesn't contain all the numbers [1,9] return false
        return column_set


    def get_sub_square_set(self,row,col):
        #Returns a set of all the current alements in a sub square
        sub_square = list()

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print "Checking sub square..."

        # find every number sub square
        col_start = col*self.SUDOKU_SUB_SIZE
        row_start = row*self.SUDOKU_SUB_SIZE
        for col in xrange(col_start, col_start + self.SUDOKU_SUB_SIZE):
            for row in xrange(row_start, row_start + self.SUDOKU_SUB_SIZE):
                sub_square.append(self.state[row][col])

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print sub_square

        # convert that row to a set for easy comparison
        sub_square_set = set(sub_square)

        # if our row doesn't contain all the numbers [1,9] return false
        return sub_square_set


    def get_super_set(self, row, col):
        #Get the corresponding row_set
        row_set = self.get_row_set(row)

        #Get the corresponding col_set
        col_set = self.get_column_set(col)

        #Converting the corresponding row and column to a subset of the sudoku
        sub_square_set = \
            self.get_sub_square_set(row/self.SUDOKU_SUB_SIZE,col/self.SUDOKU_SUB_SIZE)

        #Create a super set of row, column, and sub_square sets
        super_set = row_set
        super_set.update(col_set)
        super_set.update(sub_square_set)

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print super_set

        return super_set


    # may return TRUE in the presence of blanks
    def valid_column(self, column_number):
        column = dict()
        valid = True

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print "Checking col..."

        # use a dictionary to check for repeated numbers in our column
        for row in xrange(0, self.SUDOKU_SIDE_LENGTH):
            cur_value = self.state[row][column_number]

            if cur_value != '0':
                if cur_value in column:
                    valid = False
                    break;
                else:
                    column[cur_value] = cur_value

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print column

        return valid


    # may return TRUE in the presence of blanks
    def valid_row(self, row_number):
        row = dict()
        valid = True

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print "Checking col..."

        # use a dictionary to check for repeated numbers in our row
        for col in xrange(0, self.SUDOKU_SIDE_LENGTH):
            cur_value = self.state[row_number][col]

            if cur_value != '0':
                if cur_value in row:
                    valid = False
                    break;
                else:
                    row[cur_value] = cur_value

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print row

        return valid


    # may return TRUE in the presence of blanks
    def valid_sub_square(self, row, col):
        sub_square = dict()
        valid = True

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print "Checking sub square..."

        # find every number sub square
        col_start = col*self.SUDOKU_SUB_SIZE
        row_start = row*self.SUDOKU_SUB_SIZE
        for col in xrange(col_start, col_start + self.SUDOKU_SUB_SIZE):
            for row in xrange(row_start, row_start + self.SUDOKU_SUB_SIZE):
                cur_value = self.state[row][col]

                if cur_value != '0':
                    if cur_value in sub_square:
                        valid = False
                        break;
                    else:
                        sub_square[cur_value] = cur_value

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print sub_square

        return valid


    # may return TRUE in the presence of blanks
    def valid_sudoku(self):
        valid = True

        # check all our sub squares in range [0, 2]
        for i in xrange(0, self.SUDOKU_SUB_SIZE):
            for j in xrange(0, self.SUDOKU_SUB_SIZE):
                valid = self.valid_sub_square(i, j)

                if not valid:
                    break;

            if not valid:
                break;

        # check all of our rows and columns
        if valid:
            for i in xrange(0, self.SUDOKU_SIDE_LENGTH):
                valid = self.valid_column(i) and self.valid_row(i)

                if not valid:
                    break;

        return valid


    # returns FALSE in the presence of blanks
    def solved_column(self, column_number):
        column = list()
        valid = True

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print "Checking col..."

        # find every number in our column
        for row in xrange(0, self.SUDOKU_SIDE_LENGTH):
            cur_value = self.state[row][column_number]
            if cur_value != '0':
                if cur_value in column:
                    valid = False
            column.append(cur_value)

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print column

        # convert that column to a set for easy comparison
        column_set = set(column)

        # if our column doesn't contain all the numbers [1,9] return false
        return (len(column_set.difference(self.SUDOKU_SET)) == 0) and valid


    # returns FALSE in the presence of blanks
    def solved_row(self, row_number):
        row = list()
        valid = True

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print "Checking row..."

        # find every number in our row
        for col in xrange(0, self.SUDOKU_SIDE_LENGTH):
            cur_value = self.state[row_number][col]
            if cur_value != '0':
                if cur_value in row:
                    valid = False
            row.append(cur_value)

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print row

        # convert that row to a set for easy comparison
        row_set = set(row)

        # if our row doesn't contain all the numbers [1,9] return false
        return (len(row_set.difference(self.SUDOKU_SET)) == 0) and valid


    # returns FALSE in the presence of blanks
    def solved_sub_square(self, row, col):
        sub_square = list()
        valid = True

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print "Checking sub square..."

        # find every number sub square
        col_start = col*self.SUDOKU_SUB_SIZE
        row_start = row*self.SUDOKU_SUB_SIZE
        for col in xrange(col_start, col_start + self.SUDOKU_SUB_SIZE):
            for row in xrange(row_start, row_start + self.SUDOKU_SUB_SIZE):
                cur_value = self.state[row][col]
                if cur_value != '0':
                    if cur_value in sub_square:
                        valid = False
                sub_square.append(cur_value)

        if PRINT_STATEMENTS and DEBUG_LEVEL >= 3:
            print sub_square

        # convert that row to a set for easy comparison
        sub_square_set = set(sub_square)

        # if our row doesn't contain all the numbers [1,9] return false
        return (len(sub_square_set.difference(self.SUDOKU_SET)) == 0) and valid


    # returns FALSE in the presence of blanks
    def solved_sudoku(self):
        valid = True

        # check all our sub squares in range [0, 2]
        for i in xrange(0, self.SUDOKU_SUB_SIZE):
            for j in xrange(0, self.SUDOKU_SUB_SIZE):
                valid = self.solved_sub_square(i, j)

                if not valid:
                    break;

            if not valid:
                break;

        # check all of our rows and columns
        if valid:
            for i in xrange(0, self.SUDOKU_SIDE_LENGTH):
                valid = self.solved_column(i) and self.solved_row(i)

                if not valid:
                    break;

        return valid


    # search through our sudoku and find all the blank spaces (the 0s)
    def get_next_zero(self):
        zero_locations = list()

        for i in xrange(0, self.SUDOKU_SIDE_LENGTH):
            for j in xrange(0, self.SUDOKU_SIDE_LENGTH):
                if self.state[i][j] == '0':
                    zero_locations.append((i,j))

        return zero_locations


    def set_cur_state(self, state):
        self.cur_state = copy.deepcopy(state)


    def get_state(self):
        return Sudoku.sudoku_array_to_str(self.state)

    def get_state_file(self):
        return Sudoku.sudoku_array_to_str_file(self.state)


    def print_state(self):
        print self.get_state()


    def start_timer(self):
        self.starting_time = time.clock()

    def start_origin_timer(self):
        self.origin_time = time.clock()


    def end_timer(self):
        delta = time.clock() - self.starting_time
        return delta

    def end_origin_timer(self):
        delta = time.clock() - self.origin_time
        return delta


    def get_all_tiles(self, cur_state, zero_location):
        return list(self.SUDOKU_SET)


    def get_valid_tiles(self, cur_state, zero_location):
        # get all the numbers in the row, col, and sub_square of our current 0 position
        valid_set = self.get_super_set(zero_location[0], zero_location[1])

        # find the difference between all possible numbers and our superset of
        # currently present numbers
        valid_set = self.SUDOKU_SET.difference(valid_set)

        return list(valid_set)


def solve_sudoku(cur_state, successor_function, tile_filling_function):
    if PRINT_STATEMENTS:
        print "Current state: ", cur_state.get_state()
        print "Valid state: ", cur_state.valid_sudoku()
        print "Solved sudoku: ", cur_state.solved_sudoku()

    # if the puzzle is solved we are done
    if cur_state.solved_sudoku():
        return True, cur_state

    if not cur_state.valid_sudoku():
        return False, cur_state

    # if it isn't solved yet, find the zeros and try different solutions
    zero_locations = cur_state.get_next_zero()

    # make sure there are zeros left on the board
    # in the case we aren't done but there are no zeros left
    # something very very bad has happend....
    if len(zero_locations) == 0:
        print "BROKEN"
        cur_state.print_state()
        return False, cur_state
    else:
        zero_location = zero_locations.pop(0)


    possible_tiles = successor_function(cur_state, zero_location)


    original_state = copy.deepcopy(cur_state.state)
    for possible_tile in possible_tiles:
        tile_filled = tile_filling_function(zero_location[0], \
                                            zero_location[1], \
                                            possible_tile)
        if tile_filled:
            result, final_state = solve_sudoku(cur_state,
                                               successor_function,
                                               tile_filling_function)

            if PRINT_STATEMENTS:
                print "Result condition: ", result

            if result:
                return True, final_state
            else:
                cur_state.state = copy.deepcopy(original_state)

    return False, cur_state

def get_puzzles_from_file(puzzles_folder, puzzles_file):
    # defined by the file format
    # first line is the name followed by the 9 number lines
    LINES_PER_PUZZLE = 10
    sudoku_puzzles = list()

    # open our file containing our list of puzzles
    with open(puzzles_folder + puzzles_file, "r") as puzzles:

        for puzzle in iter(lambda: tuple(islice(puzzles, LINES_PER_PUZZLE)), ()):
            # trim the name and join each line of the puzzle into one long str
            puzzle_str = ''.join([str(puzzle_line).strip() for puzzle_line in puzzle[1:]])

            # make a new sudoku object from the string and add it to our list
            sudoku_array = Sudoku.str_to_sudoku_array(puzzle_str)
            sudoku_puzzle = Sudoku(sudoku_array)
            sudoku_puzzles.append(sudoku_puzzle)

    return sudoku_puzzles

def create_file(solved_puzzles):
    # f = open('arc_consistency.txt','w')
    f = open('backtracking.txt','w')
    puzzle_number = 1
    for puzzle in solved_puzzles:
        f.write('Grid ' +str(puzzle_number) + '\n')
        for line in puzzle:
            f.write(line)
        puzzle_number += 1


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    puzzles_folder = './'
    output_result = list()
    if DEBUG_LEVEL == 2:
        puzzles_files = ['solved_sudoku.txt']
    elif DEBUG_LEVEL == 1:
        # puzzles_files = ['50sudoku.txt']
        puzzles_files = ['1sudoku.txt']
        #puzzles_files = ['1step.txt']
    else:
        puzzles_files = ['50sudoku.txt']

    for puzzles_file in puzzles_files:
        sudoku_puzzles = get_puzzles_from_file(puzzles_folder, puzzles_file)
        sudoku_puzzles[0].print_state()
        sudoku_puzzles[0].start_origin_timer()
        for sudoku_puzzle in sudoku_puzzles:
            sudoku_puzzle.start_timer()
            print "Initial state: ",sudoku_puzzle.get_state()
            # success, puzzle_result = \
            #    solve_sudoku(sudoku_puzzle, \
            #    sudoku_puzzle.get_valid_tiles, \
            #    sudoku_puzzle.fill_in_tile)
            success, puzzle_result = \
                solve_sudoku(sudoku_puzzle, \
                sudoku_puzzle.get_all_tiles, \
                sudoku_puzzle.fill_in_tile_blind)
            duration = sudoku_puzzle.end_timer()
            print "Solved Puzzle: " + str(success) + '\n' + puzzle_result.get_state()
            print "The algorithm took ", duration, " seconds"
            output_result.append(puzzle_result.get_state_file())
        total_duration = sudoku_puzzles[0].end_origin_timer()
        print "The total ", len(sudoku_puzzles)," puzzles took ", \
            total_duration, " seconds "
        create_file(output_result)
