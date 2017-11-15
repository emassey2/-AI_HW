#!/usr/bin/env python

# I really wish python had enums...
class Direction(object):
    # Directions are described as a pair of row, col movements
    UP      = [-1,  0]
    DOWN    = [ 1,  0]
    LEFT    = [ 0, -1]
    RIGHT   = [ 0,  1]

    ROW = 0
    COL = 1

    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

class eight_puzzle:
    PUZZLE_SIDE_LENGTH = 3

    # Define some constants for our move directions


    def __init__(self, initial_state_str, goal_state_str):
        # state is represented by a 3x3 matrix
        self.cur_state = self.str_to_twoD_array(initial_state_str)
        self.goal_state = self.str_to_twoD_array(goal_state_str)


    def str_to_twoD_array(self, state_str):
        twoD_array = []
        for i in xrange(0, self.PUZZLE_SIDE_LENGTH):
            twoD_array.append([])
            for j in xrange(0, self.PUZZLE_SIDE_LENGTH):
                twoD_array[i].append(state_str[i*self.PUZZLE_SIDE_LENGTH+j])

        return twoD_array


    def twoD_array_to_str(self, twoD_array):
        state_str = ""
        for i in xrange(0, self.PUZZLE_SIDE_LENGTH):
            for j in xrange(0, self.PUZZLE_SIDE_LENGTH):
                state_str += str(twoD_array[i][j])
                state_str += ' '
            state_str += '\n'

        return state_str


    # find each number and also it's index
    def get_number_positions(self, twoD_array):
        position_list = list()

        for i in xrange(0, self.PUZZLE_SIDE_LENGTH):
            for j in xrange(0, self.PUZZLE_SIDE_LENGTH):
                position_list.append((twoD_array[i][j], i, j))

        position_list.sort()
        return position_list


    def is_valid_move(self, blank_location, move_direction):
        valid_move = True
        row = blank_location[0]
        col = blank_location[1]

        # do a pre check, to make sure we our current blank location is okay
        if row < 0 or row >= self.PUZZLE_SIDE_LENGTH \
           or col < 0 or col >= self.PUZZLE_SIDE_LENGTH:
           valid_move = False

        # check if our inteded position actually contains a tile/is valid
        new_row = row + move_direction[Direction.ROW]
        new_col = col + move_direction[Direction.COL]

        if new_row < 0 or new_row >= self.PUZZLE_SIDE_LENGTH \
           or new_col < 0 or new_col >= self.PUZZLE_SIDE_LENGTH:
           valid_move = False

        return valid_move


    def get_blank_position(self):
        blank_position = self.get_number_positions(self.cur_state)[0]
        blank_row = blank_position[1]
        blank_col = blank_position[2]

        return (blank_row, blank_col)


    # returns a 2d array that represents what moving a tile would result in
    def get_state_post_move(self, direction):
        blank_row, blank_col = self.get_blank_position()
        number_row  = blank_row + direction[0]
        number_col  = blank_col + direction[1]

        blank_tile = self.cur_state[blank_row][blank_col]
        new_state = self.cur_state

        # switch the blank tile and the number tile
        new_state[blank_row][blank_col] = new_state[number_row][number_col]
        new_state[number_row][number_col] = blank_tile

        return new_state


    # returns all possible future states (doing only one move)
    def get_possible_moves(self):
        possible_moves = list()
        blank_row, blank_col = self.get_blank_position()

        for move in Direction.DIRECTIONS:
            if self.is_valid_move((blank_row, blank_col), move):
                possible_moves.append(self.get_state_post_move(move))

        return possible_moves

    def get_manhattan_dist(self):
        cur_positions = self.get_number_positions(self.cur_state)
        goal_positions = self.get_number_positions(self.goal_state)

        distance = 0

        # sum the distance between our two states
        for i in xrange(0, self.PUZZLE_SIDE_LENGTH**2):
            distance += abs(cur_positions[i][1] - goal_positions[i][1]) + \
                        abs(cur_positions[i][2] - goal_positions[i][2])

        return distance


    def get_num_misplaced_tiles(self):
        cur_positions = self.get_number_positions(self.cur_state)
        goal_positions = self.get_number_positions(self.goal_state)

        misplaced_tiles = 0

        # add one for each misplaced tile (compare x,y cords)
        for i in xrange(0, self.PUZZLE_SIDE_LENGTH**2):
            if (cur_positions[i][1] != goal_positions[i][1] or \
                cur_positions[i][2] != goal_positions[i][2]):
                misplaced_tiles += 1

        return misplaced_tiles


    def get_state(self):
        return self.twoD_array_to_str(self.cur_state)


    def print_state(self):
        print self.get_state()

if __name__ == '__main__':
    puzzle = eight_puzzle("012345678", "876543120")
    puzzle.print_state()
    print puzzle.twoD_array_to_str(puzzle.goal_state)
    print puzzle.get_manhattan_dist()
    print puzzle.get_num_misplaced_tiles()
    print '\n'
    moves =  puzzle.get_possible_moves()
    for move in moves:
        print puzzle.twoD_array_to_str(move)
