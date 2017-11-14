#!/usr/bin/env python

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

    def get_number_positions(self, twoD_array):
        position_list = list()

        # find each number and also it's index appending it to our list
        for i in xrange(0, self.PUZZLE_SIDE_LENGTH):
            for j in xrange(0, self.PUZZLE_SIDE_LENGTH):
                position_list.append((twoD_array[i][j], i, j))

        position_list.sort()
        return position_list

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
