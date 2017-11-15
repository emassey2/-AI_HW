#!/usr/bin/env python

import copy
import sys

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


    def set_cur_state(self, state):
        self.cur_state = copy.deepcopy(state)


    # find each number and also it's index
    # return them sorted (lowest first)
    def get_number_positions(self, twoD_array):
        position_list = list()

        for row in xrange(0, self.PUZZLE_SIDE_LENGTH):
            for col in xrange(0, self.PUZZLE_SIDE_LENGTH):
                position_list.append((twoD_array[row][col], row, col))

        position_list.sort()
        return position_list


    def is_valid_move(self, blank_location, move_direction):
        valid_move = True
        blank_row = blank_location[0]
        blank_col = blank_location[1]

        # do a pre check, to make sure we our current blank location is okay
        if blank_row < 0 or blank_row >= self.PUZZLE_SIDE_LENGTH \
           or blank_col < 0 or blank_col >= self.PUZZLE_SIDE_LENGTH:
           valid_move = False

        # check if our intended position actually contains a tile/is valid
        new_row = blank_row + move_direction[Direction.ROW]
        new_col = blank_col + move_direction[Direction.COL]

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
        new_state = copy.deepcopy(self.cur_state)

        # switch the blank tile and the number tile
        new_state[blank_row][blank_col] = new_state[number_row][number_col]
        new_state[number_row][number_col] = blank_tile

        return new_state


    # returns all possible future states (doing only one move)
    def get_one_move_states(self):
        possible_states = list()
        blank_row, blank_col = self.get_blank_position()

        for move in Direction.DIRECTIONS:
            if self.is_valid_move((blank_row, blank_col), move):
                possible_states.append(self.get_state_post_move(move))

        return possible_states


    def get_state(self):
        return self.twoD_array_to_str(self.cur_state)


    def print_state(self):
        print self.get_state()



def get_manhattan_dist(cur_puzzle, cur_state, goal_state):
    cur_positions = cur_puzzle.get_number_positions(cur_state)
    goal_positions = cur_puzzle.get_number_positions(goal_state)

    distance = 0

    # sum the distance between our two states
    for i in xrange(0, puzzle.PUZZLE_SIDE_LENGTH**2):
        distance += abs(cur_positions[i][1] - goal_positions[i][1]) \
                  + abs(cur_positions[i][2] - goal_positions[i][2])

    return distance


def get_num_misplaced_tiles(cur_puzzle, cur_state, goal_state):
    cur_positions = cur_puzzle.get_number_positions(cur_state)
    goal_positions = cur_puzzle.get_number_positions(goal_state)

    misplaced_tiles = 0

    # add one for each misplaced tile (compare x,y cords)
    for i in xrange(0, cur_puzzle.PUZZLE_SIDE_LENGTH**2):
        if (cur_positions[i][1] != goal_positions[i][1] \
            or cur_positions[i][2] != goal_positions[i][2]):
            misplaced_tiles += 1

    return misplaced_tiles


def greedy_search(puzzle, heuristic, previous_states):
    goal_achieved = False

    # check for our goal state
    score = heuristic(puzzle, puzzle.cur_state, puzzle.goal_state)
    if score == 0:
        goal_achieved = True

    #print "cur_score", score, "\nState\n", puzzle.twoD_array_to_str(puzzle.cur_state)


    # if we haven't found our goal, explore our state spaces
    if not goal_achieved:
        # first we get all of our possible moves
        possible_states = puzzle.get_one_move_states()

        # evaluate all of the moves
        ranked_states = list()
        for state in possible_states:
            heuristic_score = heuristic(puzzle, state, puzzle.goal_state)
            ranked_states.append((heuristic_score, state))

        # sort and choose the first (best) move
        ranked_states.sort()
        top_ranked_state = ranked_states[0]
        #print top_ranked_state[0], top_ranked_state[1]

        # because we are greedy do the best move
        puzzle.set_cur_state(top_ranked_state[1])
        previous_states.append(top_ranked_state)
        goal_achieved = greedy_search(puzzle, heuristic, previous_states)

    return goal_achieved



if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    easy_puzzle = eight_puzzle("876514203", "876543210")
    hard_puzzle = eight_puzzle("148362057", "876543210")
    puzzles = [easy_puzzle, hard_puzzle]
    for cur_puzzle in puzzles:
        puzzle = copy.deepcopy(cur_puzzle)
        print "Starting State"
        puzzle.print_state()
        print "Goal State"
        print puzzle.twoD_array_to_str(puzzle.goal_state)
        heuristics = [(get_num_misplaced_tiles, "misplaced tiles"), \
                      (get_manhattan_dist, "manhattand distance")]
        for heuristic in heuristics:
            states = list()
            print "\n\nTrying ", heuristic[1]
            greedy_search(puzzle, heuristic[0], states)
            print "Final State"
            puzzle.print_state()

            print "Path States"
            for state in states:
                print "Heuristic:", state[0], "\nState:\n", puzzle.twoD_array_to_str(state[1])
            print "Press enter to continue"
            raw_input()
            puzzle = copy.deepcopy(cur_puzzle)
