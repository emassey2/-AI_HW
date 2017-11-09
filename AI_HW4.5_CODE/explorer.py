#!/usr/bin/env python

import os
import time
import datetime
import sys

UNEXPLORED = 0
EXPLORED = 1
PATH = 2

# change string color in terminal taken from:
# https://stackoverflow.com/questions/2330245/python-change-text-color-in-shell
def hilite(string, status, bold):
    attr = []
    if status == EXPLORED:
        # green
        attr.append('32')
    elif status == PATH:
        # blue
        attr.append('34')
    else:
        # red
        attr.append('31')

    if bold:
        attr.append('1')

    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

class Explorer:

    DFS_ITR_TYPE = 0
    DEBUG_LEVEL = 0
    SUCCESS = 0
    LIMITED = 1
    FAILURE = 2

    def __init__(self, explorer_map, goal_char='*', free_char=' ', start_char='s', debug=False):
        self.starting_time = 0
        self.cur_pos = (0, 0)
        self.goals = list()
        self.goal_char  = goal_char
        self.free_char  = free_char
        self.start_char = start_char
        self.explored_positions = dict()
        self.move_list = list()
        self.goals = list()
        self.num_steps = 0
        self.explorer_map = explorer_map
        self.debug = debug

    def start_timer(self):
        self.starting_time = datetime.datetime.now()

    def end_timer(self):
        delta = datetime.datetime.now() - self.starting_time
        return delta.microseconds

    # loop through the map and find the goals and starting position
    #I would suggest changing the find_POIS to mine, with getting the lines
    #Instead of iterating 2 times
    #But we gotta choose one before running the code, my part need my structure

    def set_goal_char(self, goal_char):
        self.goal_char = goal_char

    def weak_reset(self, goal_char='*', free_char=' ', start_char='s'):
        self.explored_positions = dict()
        self.move_list = list()
        self.num_steps = 0

    def reset(self, goal_char='*', free_char=' ', start_char='s'):
        self.starting_time = 0
        self.cur_pos = (0, 0)
        self.goals = list()
        self.explored_positions = dict()
        self.move_list = list()
        self.num_steps = 0
        self.goal_char = goal_char
        self.free_char = free_char
        self.start_char= start_char

    def find_POIs(self):
        start_found = False
        # ironic we have to search for the start...
        cur_map = self.explorer_map.explorer_map
        for col in range(0, len(cur_map)):
            for row in range(0, len(cur_map[col])):
                cur_char = cur_map[col][row]
                if cur_char == self.start_char:
                    self.cur_pos = (row, col)
                    start_found = True

                if cur_char.isdigit():
                    self.goals.append((cur_char, (row, col)))


        self.goals.sort()

        return start_found and len(self.goals) != 0


    def get_explored_map(self, debug=False):
        map_state = ''

        cur_map = self.explorer_map.explorer_map
        for i in range(0, len(cur_map)):
            for j in range(0, len(cur_map[i])):
                cur_char = cur_map[i][j]
                bold = False

                if cur_char == ' ':
                    cur_char = '0'

                if self.cur_pos == (j, i):
                    bold = True

                    # display R for robot (unless it's on a *, then it's an X)
                    if cur_char != '*':
                        cur_char = 'R'
                    else:
                        cur_char = 'X'

                tile_type = UNEXPLORED
                if (j, i) in self.explored_positions:
                    tile_type = EXPLORED
                if (j, i) in self.move_list:
                    tile_type = PATH

                map_state += \
                hilite(cur_char, tile_type, bold)
            map_state += '\n'

        if self.DEBUG_LEVEL >= 2:
            map_state += "\nCurrent Position: " + str(self.cur_pos)
            map_state += "\nSteps taken: " + str(self.num_steps)
            map_state += "\nExplored: "
            keys = self.explored_positions.keys()
            keys.sort()
            for key in keys:
                map_state += str(key) + ", "


        return map_state

    def print_explored_map(self, debug=False):
        if debug and self.DEBUG_LEVEL <= 1:
            os.system("clear")

        print self.get_explored_map(debug)

        if debug and self.DEBUG_LEVEL <= 1:
            time.sleep(.05)

    def explore(self, explore_types):
        for explore_type in explore_types:

            print "\n********************************************************************************"
            if explore_type == self.DFS_ITR_TYPE:
                search_type = "Iterative Depth-First Search"
            else:
                print "That isn't a valid search type!"
                # I will not stand for this!
                return

            # We ironically must explore the map to find the start and num goals
            if not self.find_POIs():
                print "Something has gone wrong!"
                print "I couldn't find a start or goal!"

            goal_number = 0
            while len(self.goals) > 0:
                search_result = False
                cur_goal = self.goals.pop(0)
                # update our the goal we are looking for
                cur_goal_char = cur_goal[0]
                cur_goal_pos = cur_goal[1]
                self.set_goal_char(cur_goal_char)

                print "I'll be searching for: " + str(cur_goal_char)
                print "Looks like I'll be doing a " + search_type + "!"
                print "I'll be starting at " + str(self.cur_pos)

                print "Starting the timer...now!"
                self.start_timer()
                if explore_type == self.DFS_ITR_TYPE:
                    search_result, max_lvl = self.DFS_ITR()

                self.print_explored_map()

                # convert microsecond to millisecond
                duration = self.end_timer() / 1000

                print "It took me " + str(duration) \
                    + " milliseconds to finish a " + search_type
                if explore_type == self.DFS_ITR_TYPE:
                    print "I explored " + str(len(self.explored_positions)) \
                        + " positions before finishing my search."
                print "The exploration took " + str(self.num_steps) + " steps."
                print "It will take " + str(len(self.move_list)) + \
                    " step(s) to reach our goal."

                result_string = "FAILURE"
                if search_result == self.SUCCESS:
                    result_string = "SUCCESS"
                elif search_result == self.LIMITED:
                    result_string = "LIMITED"

                print "The search was a " + result_string + "!"

                # if the search failed we need to skip the next goal
#                if search_result != self.SUCCESS and len(self.goals) > 0:
#                    self.goals.pop(0)

                # only change our start position if we were successful
                if search_result == self.SUCCESS:
                    self.cur_pos = cur_goal_pos

                # reset in prep for the next search
                self.weak_reset()

    def valid_new_exploration(self, x, y):
        valid_new_exploration = False

        #print (x, y)

        cur_char = self.explorer_map.get_char(x, y)
        if (cur_char in self.goal_char or \
           cur_char in self.free_char or \
           cur_char.isdigit() or \
           cur_char in self.start_char) \
           and (x, y) not in self.explored_positions:
            valid_new_exploration = True

        return valid_new_exploration

    def DFS_ITR(self):
        still_seraching = True
        max_lvl = 0
        result = self.FAILURE

        while still_seraching:
            result = self.DFS_ITR_recursive(0, max_lvl)

            # check if we have found our goal or exhausted our map
            if result == self.FAILURE or result == self.SUCCESS:
                still_seraching = False
            else:
                # if we didn't fail or succeed we keep searching
                max_lvl += 1
                if self.DEBUG_LEVEL >= 1:
                    self.print_explored_map()
                self.weak_reset()

        return result, max_lvl


    # returns true when we find all the goal
    def DFS_ITR_recursive(self, cur_lvl, max_lvl):
        if self.debug and self.DEBUG_LEVEL >= 2:
            self.print_explored_map(debug=True)

        # update our new position and find the current character
        cur_row = self.cur_pos[0]
        cur_col = self.cur_pos[1]
        cur_char = self.explorer_map.get_char(cur_row, cur_col)

        # add our position to our list of moves
        self.move_list.append((cur_row, cur_col))

        # mark our position as visited
        self.explored_positions[(cur_row, cur_col)] = cur_char

        # check if this is the goal
        if cur_char == self.goal_char:
            return self.SUCCESS

        # check if we are being limited (reached our max level)
        if cur_lvl >= max_lvl:
            # we are stuck and need to go back so remove this move
            self.move_list.pop()
            return self.LIMITED

        search_result = self.FAILURE
        sub_search_result = search_result

        # check down
        if self.valid_new_exploration(cur_row, cur_col+1) \
            and search_result != self.SUCCESS:
            self.num_steps += 1
            self.cur_pos = (cur_row, cur_col+1)
            sub_search_result = self.DFS_ITR_recursive(cur_lvl+1, max_lvl)
            search_result = min(sub_search_result, search_result)
            self.num_steps += 1
            self.cur_pos = (cur_row, cur_col)

            if self.debug and self.DEBUG_LEVEL >=2:
                self.print_explored_map(debug=True)

        # check right
        if self.valid_new_exploration(cur_row+1, cur_col) \
            and search_result != self.SUCCESS:
            self.num_steps += 1
            self.cur_pos = (cur_row+1, cur_col)
            sub_search_result = self.DFS_ITR_recursive(cur_lvl+1, max_lvl)
            search_result = min(sub_search_result, search_result)
            self.num_steps += 1
            self.cur_pos = (cur_row, cur_col)

            if self.debug and self.DEBUG_LEVEL >=2:
                self.print_explored_map(debug=True)

        # check left
        if self.valid_new_exploration(cur_row-1, cur_col) \
            and search_result != self.SUCCESS:
            self.num_steps += 1
            self.cur_pos = (cur_row-1, cur_col)
            sub_search_result = self.DFS_ITR_recursive(cur_lvl+1, max_lvl)
            search_result = min(sub_search_result, search_result)
            self.num_steps += 1
            self.cur_pos = (cur_row, cur_col)

            if self.debug and self.DEBUG_LEVEL >=2:
                self.print_explored_map(debug=True)

        # check up
        if self.valid_new_exploration(cur_row, cur_col-1) \
            and search_result != self.SUCCESS:
            self.num_steps += 1
            self.cur_pos = (cur_row, cur_col-1)
            sub_search_result = self.DFS_ITR_recursive(cur_lvl+1, max_lvl)
            search_result = min(sub_search_result, search_result)
            self.num_steps += 1
            self.cur_pos = (cur_row, cur_col)

            if self.debug and self.DEBUG_LEVEL >=2:
                self.print_explored_map(debug=True)

        if search_result != self.SUCCESS:
            # if we've tried every move and failed remove our position
            self.move_list.pop()

        return search_result

# a 2d array of characters for the explorer to explore
class Explorer_Map:
    def __init__(self, map_location):
        self.explorer_map = [['']]
        with open(map_location) as map_file:
            # Sometimes things would be easier/more readable in C...
            # I just wanted to make a 2d array, how did it end up like this?
            self.explorer_map = \
                [c for c in [line.rstrip("\n") for line in map_file]]

    # return a string of what our map looks like
    def to_string(self):
        map_string = ""
        for line in self.explorer_map:
            map_string += line + '\n'

        return map_string

    def get_char(self, x_pos, y_pos):
        # if you access something out of bounds you are on your own
        return self.explorer_map[y_pos][x_pos]

# try exploring all the maps provided in the folder
def test(folder, files):
    # convert all our files into Explorer_Maps and explore them
    for file_name in files:
        explorer_map = Explorer_Map(folder + file_name)
        explorer = Explorer(explorer_map)
        print "\n********************************************************************************"
        print "Trying to explore a new map!"
        print "It looks like this..."
        print explorer_map.to_string()
        search_types = list()
        search_types.append(explorer.DFS_ITR_TYPE)
        explorer.explore(search_types)

        print "********************************************************************************\n"

    raw_input("Press any key to run the first map in debug mode!")
    try:
        input= raw_input
    except NameError:
        pass

    print "\n********************************************************************************"
    print "Running an example in debug mode!"
    debug_explorer = Explorer(Explorer_Map(folder + files[0]), debug=True)
    debug_explorer.DEBUG_LEVEL = 1
    debug_search_types = list()
    debug_search_types.append(debug_explorer.DFS_ITR_TYPE)
    debug_explorer.explore(search_types)
    debug_explorer.explore(debug_search_types)
    print "********************************************************************************\n"

if __name__ == '__main__':
    #TODO probably switch to iterative...
    sys.setrecursionlimit(20000)
    files = ["map1.txt", "map2.txt", "map3.txt"]
    map_folder = "./maps/"
    test(map_folder, files)
