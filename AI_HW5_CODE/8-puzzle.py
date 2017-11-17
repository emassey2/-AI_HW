#!/usr/bin/env python

import copy
import sys
import heapq
import time
import datetime

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

class a_star_node:
    def __init__(self, puzzle,parent, movement_cost, heuristic_cost):
        #Puzzle object
        self.puzzle = puzzle
        self.parent = parent
        #g(n)
        self.movement_cost = movement_cost
        #heuristic cost h(n)
        self.heuristic_cost = heuristic_cost

    def total_cost(self):
        #Calculate the total cost of the corresponding node

        return self.movement_cost + self.heuristic_cost


class eight_puzzle:
    PUZZLE_SIDE_LENGTH = 3


    def __init__(self, initial_state, goal_state):
        # state is represented by a 3x3 matrix
        self.cur_state = initial_state
        self.goal_state = goal_state


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

    def start_timer(self):
        self.starting_time = time.clock()

    def end_timer(self):
        delta = time.clock() - self.starting_time
        return delta



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


def greedy_search(puzzle, heuristic, previous_states, path_to_goal):
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

        while len(ranked_states) != 0 and not goal_achieved:
            top_ranked_state = ranked_states.pop(0)

            # make sure we haven't visited this state before
            if top_ranked_state not in previous_states:
                # don't keep searching if we have run into a dead end
                # ie we have not states left unexplored
                # because we are greedy do the best move
                puzzle.set_cur_state(top_ranked_state[1])
                path_to_goal.append(top_ranked_state)
                previous_states.append(top_ranked_state)
                goal_achieved = greedy_search(puzzle, heuristic, previous_states, path_to_goal)

                # if we didn't find the solution remove the state we tried from our path_to_goal
                if not goal_achieved:
                    path_to_goal.pop()

        #print top_ranked_state[0], top_ranked_state[1]


    return goal_achieved

def contains_puzzle_state(puzzle_list,state):
    index = 0
    for _,a_start_object in puzzle_list:

        #Get the string corresponding to the current state
        a_start_state_str = a_start_object.puzzle.get_state()

        #Convert the state to test as a string
        state_str = a_start_object.puzzle.twoD_array_to_str(state)

        #Check if the state_str is inside the list
        # print "state string ", state_str
        # print "a_start_string", a_start_state_str
        if state_str == a_start_state_str:
            # print "same state"

            return index
        index += 1
    return -1



def a_star(puzzle, heuristic,states,path_to_goal):
    explored_states = dict()
    frontier_album = dict()
    frontier = list()

    #calculate the heuristic for the cur_state
    heuristic_score = heuristic(puzzle, puzzle.cur_state, puzzle.goal_state)
    root_node = a_star_node(puzzle,None,0,heuristic_score)

    #add root node to the frontier
    heapq.heappush(frontier,(root_node.total_cost(),root_node))
    #Add root node to the album_frontier
    frontier_album[root_node.puzzle.get_state()] = \
        (root_node.total_cost(),root_node)

    goal_achieved = False
    goal_node = None

    while (len(frontier)!=0 and not goal_achieved) :


        #Get the first element of the queue
        total_cost, cur_a_star_node = heapq.heappop(frontier)

        #Add current state to the explored_states
        explored_states[cur_a_star_node.puzzle.get_state()] = \
            (cur_a_star_node.total_cost(),cur_a_star_node)
        # explored_states.append((cur_a_star_node.total_cost(),
        #                                             cur_a_star_node))

        #Perform goal test
        if cur_a_star_node.heuristic_cost == 0:
            # print "We have fulfilled our purpose"
            goal_achieved = True
            goal_node = cur_a_star_node

        else:
            # print "Current cost: ",cur_a_star_node.movement_cost
            # print "Current heuristic: ", cur_a_star_node.heuristic_cost
            print "length of explored states: ", len(explored_states)
            #Get a list of all the possible states
            possible_states = cur_a_star_node.puzzle.get_one_move_states()

            #Evaluate all of our possible moves
            for state in possible_states:
                # print "current state \n", puzzle.twoD_array_to_str(state)
                # print "Number of explored states ", len(explored_states)
                # print "Number of elements in the frontier", len(frontier)

                #Verify if the state is in the explored list
                state_str_key = cur_a_star_node.puzzle.twoD_array_to_str(state)

                if state_str_key in explored_states:
                    state_in_previously_explored = True
                else:
                    state_in_previously_explored = False
                # state_in_previously_explored, explored_index = \
                #     contains_puzzle_state(explored_states,state)

                #Verify if the state is in the frontier

                if state_str_key in frontier_album:
                    state_in_frontier = True
                else:
                    state_in_frontier = False
                    frontier_index = contains_puzzle_state(frontier,state)

                #Calculate new movement_cost
                new_movement_cost = cur_a_star_node.movement_cost+1

                if not state_in_frontier and not state_in_previously_explored:
                    #Create a new puzzle object
                    new_puzzle = eight_puzzle(state,
                                        cur_a_star_node.puzzle.goal_state)

                    #Calculate new heuristic
                    new_heuristic = heuristic(new_puzzle,
                                                new_puzzle.cur_state,
                                                new_puzzle.goal_state)

                    #Create new a_star object
                    new_a_star_node = a_star_node(new_puzzle,
                                                   cur_a_star_node,
                                                   new_movement_cost,
                                                   new_heuristic)

                    #Push element in the frontier
                    heapq.heappush(frontier,(new_a_star_node.total_cost(),
                                            new_a_star_node))
                    frontier_album[new_a_star_node.puzzle.get_state()] = \
                            (new_a_star_node.total_cost(),new_a_star_node)


                else:
                    if state_in_frontier:
                        # print "state already in the frontier"

                        #Verify that the new movement_cost less than the current cost

                        if new_movement_cost < frontier[frontier_index][1].movement_cost:
                            # print "Removing state from frontier"
                            # print "frontier index", frontier_index
                            # print "length of the frontier", len(frontier)
                            del frontier[frontier_index]

                            heapq.heappush(frontier,(new_a_star_node.total_cost(),
                                                new_a_star_node))

                            frontier_album[new_a_star_node.puzzle.get_state()] = \
                                    (new_a_star_node.total_cost(),new_a_star_node)

                    if state_in_previously_explored:
                        # print "state already in the explored list"
                        if new_movement_cost < explored_states[state_str_key][1].movement_cost:
                            print "Removing state from explored states"
                            del explored_states[state_str_key]
                            #add the current state to the frontier
                            heapq.heappush(frontier,(new_a_star_node.total_cost(),
                                            new_a_star_node))

                            frontier_album[new_a_star_node.puzzle.get_state()] = \
                                    (new_a_star_node.total_cost(),new_a_star_node)
    if goal_achieved:
        current_node = goal_node
        while(current_node):
            path_to_goal.insert(0, (current_node.total_cost(),
                                current_node.puzzle.cur_state))
            current_node = current_node.parent
    states = explored_states
    return goal_achieved

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    initial_state_easy = [[8,7,6],[5,1,4],[2,0,3]]
    initial_state_hard = [[1,4,8],[3,6,2],[0,5,7]]
    goal_state = [[8,7,6],[5,4,3],[2,1,0]]

    easy_puzzle = eight_puzzle(initial_state_easy,goal_state)
    hard_puzzle = eight_puzzle(initial_state_hard,goal_state)

    puzzles = [easy_puzzle, hard_puzzle]
    for cur_puzzle in puzzles:
        puzzle = copy.deepcopy(cur_puzzle)
        print "Starting State"
        puzzle.print_state()
        print "Goal State"
        print puzzle.twoD_array_to_str(puzzle.goal_state)
        heuristics = [(get_manhattan_dist, "manhattand distance"), \
                      (get_num_misplaced_tiles, "misplaced tiles")]
        for heuristic in heuristics:
            states = list()
            path_to_goal = list()
            print "\n\nTrying ", heuristic[1]
            print "Starting State"
            puzzle.print_state()
            print "Starting the timer...now!"
            puzzle.start_timer()
            # greedy_search(puzzle, heuristic[0], states, path_to_goal)
            goal_achieved = a_star(puzzle,heuristic[0],states,path_to_goal)

            duration = puzzle.end_timer()
            print "It took me " + str(duration) \
                + " seconds to finish a search_type."
            # print "Final State"
            # puzzle.print_state()

            print "We explored " + str(len(states)) + " states"
            print "The path to the goal is " + str(len(path_to_goal)) + " states long"
            #print "Path to goal"
            for state in path_to_goal:
               print "Heuristic:", state[0], "\nState:\n", puzzle.twoD_array_to_str(state[1])
            print "Press enter to continue"
            raw_input()
            puzzle = copy.deepcopy(cur_puzzle)
