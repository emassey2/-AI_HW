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

class Explorer:
    def __init__(self, explorer_map, goal_char='*', free_char=' ', start_char='s'):
        self.num_goals = 0
        self.cur_pos = (0,0)
        self.free_char = free_char
        self.goals = list()
        self.explored_positions = list() #why?
        self.start_pos = (0,0)
        self.start_char = start_char
        self.goal_char = goal_char
        self.explorer_map = explorer_map
        self.num_goals_found = 0
        self.nodes_to_visit = list()


    def find_POIS(self):
        start_found = False
        a_goal_found = False
        line_ct = 0
        cur_map = self.explorer_map.explorer_map
        #Read each line as a string
        for line in cur_map:
             #Find if the character is in the line
            if self.start_char in line:
                #Get the line and position in the line of the character
                self.start_pos = (line_ct,line.index(self.start_char))
                print self.start_pos
                self.nodes_to_visit.append((self.start_pos))
                # print "Nodes to visit: ", self.nodes_to_visit
                start_found = True

            if self.goal_char in line:
                a_goal_found = True
                self.num_goals += line.count(self.goal_char)
            line_ct += 1
        print self.num_goals
        return start_found and a_goal_found

    def explore(self):
        success = False
        if not self.find_POIS():
            print "Something has gone wrong!"
            print "I couldn't find a start or goal!"
        print "I'll try to find " +str(self.num_goals) \
            + " goal(s)"

        success = self.BFS()
        # os.system('clear')
        # print self.get_explored_map()
        # time.sleep(.1)
        # for i in range(0,3):
        #     success = self.BFS()

        success_str = "success " if success else "failure"

        print "I found " + str(self.num_goals_found) + \
                " goals out of a possible " + str(self.num_goals)
        print "The search was ultimately a " + success_str + "!"


    def valid_new_exploration(self, row, column):
        valid_new_exploration = False
        cur_char = self.explorer_map.get_char(row,column)
        # print "Exploring this cell: " +cur_char
        #why in?
        #there wont be other start char, oder?
        if (cur_char in self.goal_char or\
            cur_char in self.free_char or \
            cur_char in self.start_char) \
            and (row,column) not in self.explored_positions:
            valid_new_exploration = True

        return valid_new_exploration

    def get_explored_map(self):
        map_state = ''

        cur_map = self.explorer_map.explorer_map
        for i in range(0, len(cur_map)):
            for j in range(0, len(cur_map[i])):
                cur_char = cur_map[i][j]
                bold = False

                if cur_char == ' ':
                    cur_char = '0'

                if self.cur_pos == (i, j):
                    bold = True
                    if cur_char != '*':
                        cur_char = 'R'
                    else:
                        cur_char = 'X'

                map_state += \
                    hilite(cur_char, (i, j) in self.explored_positions, bold)
            map_state += '\n'


        return map_state

    def BFS(self):
        done_exploring = False
        while (done_exploring != True and len(self.nodes_to_visit) != 0):
            # # os.system('clear')
            # print self.get_explored_map()
            time.sleep(.1)
            # print done_exploring

            #Start position
            if len(self.nodes_to_visit) !=0:
                self.cur_pos = self.nodes_to_visit.pop(0)
            print "Current position: ", self.cur_pos
            row = self.cur_pos[0]
            print "Row: ", row
            column = self.cur_pos[1]
            print "Column: ", column
            print "I'll start at row: " +str(row)
            print "and column: " +str(column)

            cur_char = self.explorer_map.get_char(row,column)

            #Mark our position as visited
            self.explored_positions.append((row,column))

            print "I've explored: ", self.explored_positions

            #Check if this position is a goal
            if cur_char == self.goal_char:
                self.num_goals_found +=1

            #Finish exploring if number of all goals are found
            if self.num_goals_found == self.num_goals: #It will never be greater
                done_exploring = True
                # break

            #Check down
            if self.valid_new_exploration(row+1, column) and not done_exploring:
                #Create a new node to visit
                if ((row+1,column) not in self.nodes_to_visit):
                    self.nodes_to_visit.append((row+1,column))

            #check right
            if self.valid_new_exploration(row, column+1) and not done_exploring:
                #Create a new node to visit
                if ((row,column+1) not in self.nodes_to_visit):
                                self.nodes_to_visit.append((row,column+1))

            #check up
            if self.valid_new_exploration(row-1, column) and not done_exploring:
                #Create a new node to visit
                if ((row-1,column) not in self.nodes_to_visit):
                    self.nodes_to_visit.append((row-1,column))

            #check left
            if self.valid_new_exploration(row, column-1) and not done_exploring:
                #Create a new node to visit
                if ((row,column-1) not in self.nodes_to_visit):
                    self.nodes_to_visit.append((row,column-1))

            print self.nodes_to_visit
        return done_exploring


class Explorer_Map:
    def __init__(self, map_location):
        # self.explorer_map = [['']]
        with open(map_location) as map_file:
            self.explorer_map = \
                [c for c in [line.rstrip("\n") for line in map_file]]

    def to_string(self):
        map_string = ""
        for line in self.explorer_map:
            map_string += line + '\n'
        return map_string

    def get_char(self, row, column):
        return self.explorer_map[row][column]

def test(folder,files):
    # for file_name in files:
    explorer_map = Explorer_Map(folder + files)
    explorer = Explorer(explorer_map)
    print "\n********************************************************************************"
    print "Trying to explore a new map!"
    print "It looks like this..."
    print explorer_map.to_string()
    # print explorer.find_POIS()
    raw_input("Press any key to run the first map in debug mode!")
    try:
        input= raw_input
    except NameError:
        pass
    explorer.explore()
print "\n********************************************************************************"
if __name__ == '__main__':
    #TODO probably switch to iterative...
    files = ["map1.txt", "map2.txt", "map3.txt"]
    map_folder = "./maps/"
    # test(map_folder, files)
    test(map_folder, "map1.txt")
