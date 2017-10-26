#!/usr/bin/env python

import os
import time
import datetime
import sys

# change string color in terminal taken from:
# https://stackoverflow.com/questions/2330245/python-change-text-color-in-shell
def hilite(string, status, bold):
    attr = []
    if status:
        # green
        attr.append('32')
    else:
        # red
        attr.append('31')
    if bold:
        attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

# explores a "map" (a 2d list of characters)
class Explorer:

    DFS_TYPE = 0
    BFS_TYPE = 1
    DEBUG_LEVEL = 1

    def __init__(self, explorer_map, goal_char='*', free_char=' ', start_char='s', debug=False):
        self.delete_me = True
        self.starting_time = 0
        self.cur_pos = (0, 0)
        self.goals = list()
        self.goal_char  = goal_char
        self.free_char  = free_char
        self.start_char = start_char
        self.explored_positions = dict()
        self.num_goals_found = 0
        self.num_goals = 0
        self.num_steps = 0
        self.explorer_map = explorer_map
        self.debug = debug
        self.ending_pos = (0,0)

    def start_timer(self):
        self.starting_time = datetime.datetime.now()

    def end_timer(self):
        delta = datetime.datetime.now() - self.starting_time
        return delta.microseconds

    # loop through the map and find the goals and starting position
    def find_POIs(self):
        start_found = False
        a_goal_found = False
        # ironic we have to search for the start...
        cur_map = self.explorer_map.explorer_map
        for i in range(0, len(cur_map)):
            for j in range(0, len(cur_map[i])):
                cur_char = cur_map[i][j]
                if cur_char == self.start_char:
                    self.cur_pos = (j, i)
                    start_found = True

                if cur_char == self.goal_char:
                    a_goal_found = True
                    self.num_goals += 1

        return start_found and a_goal_found

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

                map_state += \
                    hilite(cur_char, (j, i) in self.explored_positions, bold)
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
            time.sleep(.1)

    def explore(self, explore_types):
        for explore_type in explore_types:
            if explore_type == self.DFS_TYPE:
                search_type = "Depth-First Search"
            elif explore_type == self.DFS_TYPE:
                search_type = "Breadth-First Search"
            else:
                print "That isn't a valid search type!"
                # I will not stand for this!
                return

            # We ironically must explore the map to find the start and num goals
            if not self.find_POIs():
                print "Something has gone wrong!"
                print "I couldn't find a start or goal!"

            print "Looks like I'll be doing a " + search_type + "!"
            print "I'll be trying to find " + str(self.num_goals) \
                + " goal(s)."
            print "I'll be starting at " + str(self.cur_pos)

            print "Starting the timer...now!"
            self.start_timer()
            success = self.DFS()

            #before printing the map reset to the ending position
            if success:
                self.cur_pos = self.ending_pos
            self.print_explored_map()

            # convert microsecond to millisecond
            duration = self.end_timer() / 1000

            success_str = "success" if success else "failure"

            print "It took me " + str(duration) \
                + " milliseconds to finish a search_type."
            print "I explored " + str(len(self.explored_positions)) \
                + " positions before finding the goal(s) or giving up."
            print "The exploration took " + str(self.num_steps) + " steps."
            print "I found " + str(self.num_goals_found) + \
                " goals out of a possible " + str(self.num_goals)
            print "The search was ultimately a " + success_str + "!"

    def valid_new_exploration(self, x, y):
        valid_new_exploration = False

        #print (x, y)

        cur_char = self.explorer_map.get_char(x, y)
        if (cur_char in self.goal_char or \
           cur_char in self.free_char or \
           cur_char in self.start_char) \
           and (x, y) not in self.explored_positions:
            valid_new_exploration = True

        return valid_new_exploration

    # returns true when we find all the goals expected
    def DFS(self):
        if self.debug:
            self.print_explored_map(debug=True)
        done_exploring = False

        # update our new position and find the current character
        cur_row = self.cur_pos[0]
        cur_col = self.cur_pos[1]
        cur_char = self.explorer_map.get_char(cur_row, cur_col)

        # mark our position as visited
        self.explored_positions[(cur_row, cur_col)] = cur_char

        # check if this is the goal
        if cur_char == self.goal_char:
            self.num_goals_found += 1

        # return if we have met our expected goal
        if self.num_goals_found >= self.num_goals:
            done_exploring = True
            self.ending_pos = (cur_row, cur_col)

        # check down
        if self.valid_new_exploration(cur_row, cur_col+1) and not done_exploring:
            self.num_steps += 1
            self.cur_pos = (cur_row, cur_col+1)
            done_exploring = self.DFS()
            if not done_exploring:
                self.num_steps += 1
                self.cur_pos = (cur_row, cur_col)
                if self.debug:
                    self.print_explored_map(debug=True)

        # check right
        if self.valid_new_exploration(cur_row+1, cur_col) and not done_exploring:
            self.num_steps += 1
            self.cur_pos = (cur_row+1, cur_col)
            done_exploring = self.DFS()
            if not done_exploring:
                self.num_steps += 1
                self.cur_pos = (cur_row, cur_col)
                if self.debug:
                    self.print_explored_map(debug=True)

        # check left
        if self.valid_new_exploration(cur_row-1, cur_col) and not done_exploring:
            self.num_steps += 1
            self.cur_pos = (cur_row-1, cur_col)
            done_exploring = self.DFS()
            if not done_exploring:
                self.num_steps += 1
                self.cur_pos = (cur_row, cur_col)
                if self.debug:
                    self.print_explored_map(debug=True)

        # check up
        if self.valid_new_exploration(cur_row, cur_col-1) and not done_exploring:
            self.num_steps += 1
            self.cur_pos = (cur_row, cur_col-1)
            done_exploring = self.DFS()
            if not done_exploring:
                self.num_steps += 1
                self.cur_pos = (cur_row, cur_col)
                if self.debug:
                    self.print_explored_map(debug=True)

        # no where else to look
        return done_exploring


    def BFS(self):
        # TODO Fill in code below
        ### BFS code goes here
        ### Take a look at the DFS_TYPE as a reference
        return False

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
        explorer.explore((explorer.DFS_TYPE, explorer.BFS_TYPE))

        print "********************************************************************************\n"

    raw_input("Press any key to run the first map in debug mode!")
    try:
        input= raw_input
    except NameError:
        pass

    print "\n********************************************************************************"
    print "Running an example in debug mode!"
    debug_explorer = Explorer(Explorer_Map(folder + files[0]), debug=True)
    debug_explorer.explore((debug_explorer.DFS_TYPE, debug_explorer.BFS_TYPE))
    print "********************************************************************************\n"
if __name__ == '__main__':
    #TODO probably switch to iterative...
    sys.setrecursionlimit(20000)
    files = ["map1.txt", "map2.txt", "map3.txt"]
    map_folder = "./maps/"
    test(map_folder, files)

