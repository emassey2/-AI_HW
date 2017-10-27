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
class Node:
    def __init__(self, parent, children, position):
        self.children = children #list of objects of type node
        self.parent = parent #object type node
        self.position = position #tuple

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
        #Should we change the dict to a list?
        self.explored_positions = dict()
        self.explored_positions_l = list()
        self.num_goals_found = 0
        self.num_goals = 0
        self.num_steps = 0
        self.explorer_map = explorer_map
        self.debug = debug
        self.start_pos = (0,0)
        self.ending_pos = (0,0)
        self.nodes_to_visit = list()
        self.root = Node(None,list(),(0,0)) #Create the root

    def start_timer(self):
        self.starting_time = datetime.datetime.now()

    def end_timer(self):
        delta = datetime.datetime.now() - self.starting_time
        return delta.microseconds

    # loop through the map and find the goals and starting position
    #I would suggest changing the find_POIS to mine, with getting the lines
    #Instead of iterating 2 times
    #But we gotta choose one before running the code, my part need my structure

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

        # for line in cur_map:
        #      #Find if the character is in the line
        #     if self.start_char in line:
        #         #Get the line and position in the line of the character
        #         self.start_pos = (line_ct,line.index(self.start_char))
        #         # print self.start_pos
        #         # self.nodes_to_visit.append((self.start_pos))
        #         self.root.position = self.start_pos
        #         self.nodes_to_visit.append(self.root)
        #         # print "Nodes to visit: ", self.nodes_to_visit
        #         start_found = True
        #
        #     if self.goal_char in line:
        #         a_goal_found = True
        #         self.num_goals += line.count(self.goal_char)
        #     line_ct += 1
        # print self.num_goals
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

    #Pending to add the time and steps counter
    def BFS(self):
        done_exploring = False
        cur_node = self.root
        moves_to_do = list()

        while (done_exploring != True and len(self.nodes_to_visit) != 0):
            # # os.system('clear')
            # print self.get_explored_map()
            # time.sleep(.1)
            # print done_exploring

            #Start position
            if len(self.nodes_to_visit) !=0:
                cur_node = self.nodes_to_visit.pop(0)
            # print "Current position to explore: ", cur_node.position
            cur_row = cur_node.position[0]
            cur_col = cur_node.position[1]
            self.cur_pos = cur_node.position #Variable used to draw the map
            #Increase one step, due to movement
            # self.print_explored_map()

            cur_char = self.explorer_map.get_char(cur_row,cur_col)

            #Mark our position as visited
            if cur_node.position not in self.explored_positions:
                self.explored_positions.append((cur_row,cur_col))

            self.explored_positions.sort()

            # print "I've explored: ", self.explored_positions

            #Check if this position is a goal
            if cur_char == self.goal_char:
                self.num_goals_found +=1

            #Finish exploring if number of all goals are found
            if self.num_goals_found == self.num_goals: #It will never be greater
                done_exploring = True

            #Get the children of the current node
            if not done_exploring:
                cur_node.children = self.find_children(cur_node)
                # print "Number of children found: ", len(cur_node.children)

            if not done_exploring and len(self.nodes_to_visit) !=0:
                #Find the moves neccesary to move to the next position
                moves_to_do = self.move_to_position(cur_node,self.nodes_to_visit[0])
                # print "List of moves: ", moves_to_do
                while(len(moves_to_do) != 0):
                    #Just move back in the tree
                    #Increase 1 step for each movement
                    self.cur_pos = moves_to_do.pop(0)
                    # print "Passing by position: ", self.cur_pos
                    # self.print_explored_map()
                    # time.sleep(.1)
                # print "\n********************************************************************************"


        return done_exploring

    def nodes_to_visit_checker(self,(cur_row,cur_col)):
        down_flag = True
        up_flag = True
        right_flag = True
        left_flag = True

        for node in self.nodes_to_visit:
            # print "Node Position ", node.position
            #down
            if node.position == (cur_row+1,cur_col):
                down_flag = False
            #right
            if node.position == (cur_row,cur_col+1):
                # print "Node Position ", node.position
                # print "Current row: ", cur_row
                # print "Current col: ", cur_col+1

                right_flag = False
            #up
            if node.position == (cur_row-1,cur_col):
                up_flag = False
            #left
            if node.position == (cur_row,cur_col-1):
                left_flag = False
        return down_flag,right_flag,up_flag,left_flag

    def find_children(self, node):
        cur_pos = node.position
        cur_row = cur_pos[0]
        cur_col = cur_pos[1]
        children_list = list()

        down_flag,right_flag,up_flag,left_flag = \
            self.nodes_to_visit_checker((cur_row,cur_col))

        #Check down
        if self.valid_new_exploration(cur_row+1, cur_col) and \
            down_flag:
                down_child = Node(node, list(), (cur_row+1,cur_col))
                # print "Down child position: ", down_child.position
                children_list.append(down_child)
                self.nodes_to_visit.append(down_child)


        #check right
        if self.valid_new_exploration(cur_row, cur_col+1) and \
            right_flag:
                right_child = Node(node, list(), (cur_row, cur_col+1))
                # print "right child position: ", right_child.position
                children_list.append(right_child)
                self.nodes_to_visit.append(right_child)

        #check up
        if self.valid_new_exploration(cur_row-1, cur_col) and \
            up_flag:
                up_child = Node(node, list(), (cur_row-1, cur_col))
                # print "Up child position: ", up_child.position
                children_list.append(up_child)
                self.nodes_to_visit.append(up_child)

        #check left
        if self.valid_new_exploration(cur_row, cur_col-1) and \
            left_flag:
                left_child = Node(node, list(), (cur_row, cur_col-1))
                # print "Left child position: ", left_child.position
                children_list.append(left_child)
                self.nodes_to_visit.append(left_child)

        return children_list

    def move_to_position(self,cur_node, desired_node):
        #list of tuples (moves) based on the tree structure
        moves_to_do = list()
        moves_based_on_ancestors = list()
        ancestors = list()
        requested_cur_node = cur_node
        requested_desired_node = desired_node
        deb_desired_node_parent = desired_node.parent
        deb_cur_node_parent = cur_node.parent
        # print "The desired node :", desired_node.position
        # print "Desired node parent: ", deb_desired_node_parent.position

        while (desired_node.parent != None):
            ancestors.append(desired_node.parent)
            desired_node = desired_node.parent
            moves_based_on_ancestors.append(desired_node.position)

        # print "Number of ancestors: ", len(ancestors)

        #Get back to the original request
        desired_node = requested_desired_node

        if desired_node in cur_node.children:
            print "No additional moves required"

        else:
            # print cur_node.position, " is a child of ", \
                # deb_cur_node_parent.position
            while (cur_node not in ancestors):
                cur_node = cur_node.parent
                # print "Movement to add: ", cur_node.position
                moves_to_do.append(cur_node.position)

            #Get index of the position in the list
            index = moves_based_on_ancestors.index(cur_node.position)
            # print "Found this ancestor on the index: ", index
            #Get a sublist till the common parent
            moves_based_on_ancestors = moves_based_on_ancestors[:index]
            #Reverse moves_based_on_ancestors
            moves_based_on_ancestors = moves_based_on_ancestors[::-1]
            #Conmbine both move list
            moves_to_do = moves_to_do + moves_based_on_ancestors

        return moves_to_do
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
