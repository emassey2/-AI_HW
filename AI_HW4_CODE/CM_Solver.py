#!/usr/bin/env python

class CM:

    def __init__(self, num_cannibals, num_missonaries, num_cannibals_right = 0, num_missonaries_right = 0, max_people_per_boat = 2):
        self.MAX_PEOPLE_ON_BOAT = max_people_per_boat
        self.DEBUG = False

        self.cannibals_left = num_cannibals
        self.missonaries_left = num_missonaries

        self.cannibals_right = num_cannibals_right
        self.missonaries_right = num_missonaries_right

        self.boat_left = True

    def recursive_solver(self):
        print "test"

    def get_state(self):
        cur_state = ""
        cur_state += "C" + str(self.cannibals_left)
        cur_state += " M" + str(self.missonaries_left)

        if self.boat_left:
            cur_state += " B || "
        else:
            cur_state += " || B "

        cur_state += "C" + str(self.cannibals_right)
        cur_state += " M" + str(self.missonaries_right)

        return cur_state

    def move_people(self, num_cannibals, num_missonaries):
        valid_move = True

        # make sure we aren't trying to move more than MAX_PEOPLE_ON_BOAT
        valid_move = (num_missonaries + num_cannibals) <= self.MAX_PEOPLE_ON_BOAT

        # make sure we actually have people we can move
        if valid_move and self.boat_left:
            valid_move = (num_missonaries <= self.missonaries_left and
                num_cannibals <= self.cannibals_left)
        elif valid_move:
            valid_move = (num_missonaries <= self.missonaries_right and
                num_cannibals <= self.cannibals_right)

        # now we know this is a valid request we can move the people
        if valid_move and self.boat_left:
            self.missonaries_left -= num_missonaries
            self.missonaries_right += num_missonaries
            self.cannibals_left -= num_cannibals
            self.cannibals_right += num_cannibals
        elif valid_move:
            self.missonaries_left += num_missonaries
            self.missonaries_right -= num_missonaries
            self.cannibals_left += num_cannibals
            self.cannibals_right -= num_cannibals

        if valid_move:
            self.boat_left = not self.boat_left

        return valid_move

    def missonaries_die(self):
        return (self.missonaries_left != 0 and self.missonaries_left < self.cannibals_left) or \
            (self.missonaries_right != 0 and self.missonaries_right < self.cannibals_right)

def recursive_solver(cur_state, visited_states, solution):
    solution.append(cur_state.get_state())
    if cur_state.DEBUG:
        print "\n\n********************************************************************************"
        print "Current State:" + cur_state.get_state()
        print "Visisted States:"
        i = 0
        if cur_state.DEBUG:
            for state in visited_states:
                print str(i) + ") " + state
                i += 1

    # check for our goal state
    if (cur_state.missonaries_left == 0 and cur_state.cannibals_left == 0):
        if cur_state.DEBUG:
            print "\n\n********************************************************************************"
            print "Solution!"
            i = 0
            for state in solution:
                print str(i) + ") " + state
                i += 1
        return True

    # check to make sure no one dies. If they do this is an invalid state
    if cur_state.missonaries_die() == True:
        if cur_state.DEBUG:
            print "Missonary died"
        solution.pop()
        return False

    # make sure we don't explore a state we've already tried
    if cur_state.get_state() in visited_states:
        if cur_state.DEBUG:
            print "Already Visited: " + cur_state.get_state()
        solution.pop()
        return False
    else:
        visited_states.append(cur_state.get_state())

    # try moving each possible configuration
    people_per_boat = cur_state.MAX_PEOPLE_ON_BOAT
    while (people_per_boat > 0):
        for i in range(0, people_per_boat + 1):
            if cur_state.move_people(i, people_per_boat - i):
                if (recursive_solver(cur_state, visited_states, solution)):
                    return True
                else:
                    cur_state.move_people(i, people_per_boat - i)
        people_per_boat -= 1

    if cur_state.DEBUG:
        print "No moves left"
    solution.pop()
    return False

def basic_test():
    c3m3 = CM(3, 3)
    print c3m3.get_state()
    print c3m3.move_people(1, 1)
    print c3m3.get_state()
    print c3m3.move_people(0, 2)
    print c3m3.get_state()
    print c3m3.move_people(0, 1)
    print c3m3.get_state()
    print c3m3.missonaries_die()
    print c3m3.move_people(0, 2)
    print c3m3.get_state()
    print c3m3.missonaries_die()

def test():

    for i in range(1, 11):
        for j in range(1, 11):
            cimi = CM(i, i, max_people_per_boat=j)
            result = recursive_solver(cimi, [], [])
            print "Recursive Result for c" + str(i) + \
                "m" + str(i) + " with " + str(cimi.MAX_PEOPLE_ON_BOAT) + \
                " max people per boat: " + str(result)


if __name__ == '__main__':
    test()

