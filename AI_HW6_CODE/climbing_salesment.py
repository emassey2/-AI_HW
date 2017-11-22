#!/usr/bin/python

import re
import math
import random
import time

DEBUG_LEVEL = 1

CITY_NAME = 1
CITY_LATI = 2
CITY_LONG = 3



class City:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude



def get_cities_from_file(cities_folder, cities_file):
    cities_and_positions_list = list()

    # prepare our beautiful regex
    # this regex grabs the city name and two (possibly negative) coordinates
    city_position_regex_str = "(.+?),(-?\d+\.?\d+),(-?\d+\.?\d+)"

    # open our file containing our list of cities and their coordinates
    with open(cities_folder + cities_file, "r") as cities_and_positions:

        # iterate over all the cities
        for city_and_position in cities_and_positions:

            # attempt to grab the city name and coordinate
            match = re.match(city_position_regex_str, city_and_position)

            # make sure this line was actually a city
            if match:
                new_city = City(
                                match.group(CITY_NAME),
                          float(match.group(CITY_LATI)),
                          float(match.group(CITY_LONG)))
                # add our new city to the list of all the cities
                cities_and_positions_list.append(new_city)

    return cities_and_positions_list


def get_cities_distance(city1, city2):
    # compute the distance between two points...
    return math.sqrt(
                    pow(city1.latitude - city2.latitude, 2)
                  + pow(city1.longitude - city2.longitude, 2))


def cities_graph_from_list(cities):
    # a graph in our case is a 2D adjacency matrix

    # first we define the size of our adjacency matrix to be the number of
    # cities squared
    num_cities = len(cities)
    num_cols = num_cities
    num_rows = num_cols

    # initialize everything inside the array as -1
    cities_graph = [[-1 for x in xrange(num_cols)] for y in xrange(num_rows)]

    for i in xrange(num_cols):
        for j in xrange(num_rows):
            if cities[i] != cities[j]:
                cities_graph[i][j] = get_cities_distance(cities[i], cities[j])

    return cities_graph


# travel_plan is a list of ints that when paired with the adjacent int
# represent the distance between two cities
def calculate_round_trip(travel_plan, cities_graph):
    # in the sake of efficientcy we make some dangerous assumptions...
    # for instance, we assume we have at least 2 cities
    trip_length = len(travel_plan)
    total_distance = 0

    # the -1 is to account for looking forward one in the list
    # by subtracting 1 from the length our i will actually stop one short
    # of the length of the list and we can then manually lookup the
    # distance from the final position to our home position
    for i in xrange(0, trip_length-1):
        total_distance += cities_graph[travel_plan[i]][travel_plan[i+1]]

    # don't forget about our return home
    # pythons -1 wrap around index still scares me...
    total_distance += cities_graph[travel_plan[-1]][travel_plan[0]]

    return total_distance

def swap_random_city_with_neighbor(travel_plan):
    last_city_index = len(travel_plan) -1
    right = random.randint(0,1)

    #randomly swapping with a neighbor
    city_to_swap = random.randint(0, last_city_index)
    if (city_to_swap == 0 and right == 0) or \
       (city_to_swap == last_city_index and right == 1):
        travel_plan[0],travel_plan[-1] = travel_plan[-1], travel_plan[0]
    elif right == 1:
        travel_plan[city_to_swap],travel_plan[city_to_swap+1] = \
            travel_plan[city_to_swap+1], travel_plan[city_to_swap]
    else:
        travel_plan[city_to_swap],travel_plan[city_to_swap-1] = \
            travel_plan[city_to_swap-1], travel_plan[city_to_swap]

def swap_neighbors(travel_plan):
    neighbors = list()
    new_travel_plan = travel_plan[:]
    last_city_index = len(travel_plan) -1
    for city_to_swap in xrange(last_city_index):
        if city_to_swap == last_city_index:
            new_travel_plan[0],new_travel_plan[-1] = travel_plan[-1], travel_plan[0]
        else:
            new_travel_plan[city_to_swap],new_travel_plan[city_to_swap+1] = \
                travel_plan[city_to_swap+1], travel_plan[city_to_swap]
        neighbors.append(new_travel_plan)

        new_travel_plan = travel_plan[:]
    return neighbors

def hill_climbing (travel_plan,cities_graph,minutes,get_successor,random_restart = False):
    cur_travel_plan = travel_plan
    t_end = time.time() + 60*minutes

    cur_total_distance = calculate_round_trip(cur_travel_plan,cities_graph)
    best_neighbor_distance = cur_total_distance

    # keep looking for better neighbors while there is time and we are not at
    # a local maxima
    while (time.time() < t_end):
        # get a subset of our neighbors as defined by get_succesor
        neighbors = get_successor(cur_travel_plan)
        print len(neighbors)

        # evaluate the fitness of each neighbor
        for neighbor_travel_plan in neighbors:
            # get this neighbors fitness
            new_total_distance = calculate_round_trip(neighbor_travel_plan,cities_graph)
            # print neighbor_travel_plan

            # if this neighbor is the best we've seen update our best_neighbor
            if new_total_distance < best_neighbor_distance:
                best_neighbor_travel_plan = neighbor_travel_plan
                best_neighbor_distance = new_total_distance

        # now that we've seen all our neighbors, check to make sure we have
        # found one better than our current state
        if cur_total_distance <= best_neighbor_distance:
            # Unable to find a better neighbor!
            # in the case we are doing random restarts we get a new chance!
            if random_restart:
                    cur_travel_plan = random.sample(xrange(0, num_cities), num_cities)
                    cur_total_distance = calculate_round_trip(cur_travel_plan,cities_graph)
                    best_neighbor_distance = cur_state_distance
            else:
                return cur_total_distance
        else:
            # we've found a better neighbor and must update
            cur_total_distance = best_neighbor_distance
            cur_travel_plan = best_neighbor_travel_plan

    return cur_total_distance




if __name__ == '__main__':
    cities_folder = './graphs/'

    if DEBUG_LEVEL == 3:
        cities_files = ['3_cities.txt']
    elif DEBUG_LEVEL == 2:
        cities_files = ['9_cities.txt']
    elif DEBUG_LEVEL == 1:
        cities_files = ['49_cities.txt']
    else:
        cities_files = ['cities_full.txt']

    for cities_file in cities_files:
        cities = get_cities_from_file(cities_folder, cities_file)
        num_cities = len(cities)
        cities_graph = cities_graph_from_list(cities)

        # get a random travel_plan
        travel_plan = random.sample(xrange(0, num_cities), num_cities)
        print travel_plan
        print calculate_round_trip(travel_plan, cities_graph)
        best_total_distance = hill_climbing(travel_plan,
                                                  cities_graph,
                                                  1,
                                                  swap_neighbors)
        print travel_plan
        print best_total_distance
