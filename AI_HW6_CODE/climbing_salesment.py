#!/usr/bin/python

import re
import math
import random
import time
import matplotlib.pyplot as plt

DEBUG_LEVEL = 0
PRINT_STATEMENTS = True

CITY_NAME = 1
CITY_LONG = 2
CITY_LATI = 3



class City:
    def __init__(self, name, longitude, latitude):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude



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
                          float(match.group(CITY_LONG)),
                          float(match.group(CITY_LATI)))
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

def generate_random_plans(travel_plan):
    num_cities = len(travel_plan)
    plans = list()
    for plan in xrange(num_cities):
        plans.append(random.sample(xrange(0, num_cities), num_cities))

    return plans


# create our neighbors by swaping every city with a different random city
def swap_random_cities(travel_plan):
    neighbors = list()
    new_travel_plan = travel_plan[:]
    last_city_index = len(travel_plan) - 1

    for city_to_swap in xrange(last_city_index):
        random_city = random.randint(0,last_city_index)

        new_travel_plan[city_to_swap],new_travel_plan[random_city] \
            = travel_plan[random_city], travel_plan[city_to_swap]

        neighbors.append(new_travel_plan)

        # reset our new_travel plan as to not continue to modify the newly
        # created neighbor
        new_travel_plan = travel_plan[:]

    return neighbors


# similar two above but we choose two random cities every time
def swap_two_random_cities(travel_plan):
    neighbors = list()
    new_travel_plan = travel_plan[:]
    last_city_index = len(travel_plan) - 1

    for city_to_swap in xrange(last_city_index):
        random_city_1 = random.randint(0,last_city_index)
        random_city_2 = random.randint(0,last_city_index)

        new_travel_plan[random_city_2],new_travel_plan[random_city_1] \
            = travel_plan[random_city_1], travel_plan[random_city_2]

        neighbors.append(new_travel_plan)

        # reset our new_travel plan as to not continue to modify the newly
        # created neighbor
        new_travel_plan = travel_plan[:]

    return neighbors


# swap every city with the city to it's "right"
def swap_neighbors(travel_plan):
    neighbors = list()
    new_travel_plan = travel_plan[:]
    last_city_index = len(travel_plan) - 1

    for city_to_swap in xrange(last_city_index):
        if city_to_swap == last_city_index:
            new_travel_plan[0],new_travel_plan[-1] = travel_plan[-1], travel_plan[0]
        else:
            new_travel_plan[city_to_swap],new_travel_plan[city_to_swap+1] = \
                travel_plan[city_to_swap+1], travel_plan[city_to_swap]
        neighbors.append(new_travel_plan)

        new_travel_plan = travel_plan[:]

    return neighbors


def random_restart_hill_climbing(travel_plan, cities_graph, end_time, get_successor):
    # get a random starting path
    cur_travel_plan = travel_plan
    best_travel_plan = cur_travel_plan[:]

    cur_total_distance = calculate_round_trip(cur_travel_plan, cities_graph)
    best_total_distance = cur_total_distance

    if PRINT_STATEMENTS:
        print "best travel plan", best_travel_plan
        print "best total distance", best_total_distance

    while (time.time() < end_time):
        # basic_hill_climbing will only return if we have timed out our if
        # we have reached a local minima/maxima
        new_travel_plan, new_total_distance = basic_hill_climbing(cur_travel_plan,
                                                                 cities_graph,
                                                                 end_time,
                                                                 get_successor)
        if PRINT_STATEMENTS:
            print "new total distance", new_total_distance

        # update our current solution if we have found a better one
        if new_total_distance < best_total_distance:
            cur_total_distance = new_total_distance
            best_travel_plan = new_travel_plan[:]
            best_total_distance = new_total_distance
            if PRINT_STATEMENTS:
                print "best travel plan", best_travel_plan
                print "best total distance", best_total_distance
                print time.time(), end_time

        cur_travel_plan = random.sample(xrange(0, num_cities), num_cities)
        cur_total_distance = calculate_round_trip(cur_travel_plan, cities_graph)

    return best_travel_plan, best_total_distance


def contingency_random_restart_hill_climbing(travel_plan, cities_graph, end_time, get_successor):
    # get a random starting path
    cur_travel_plan = travel_plan
    best_travel_plan = cur_travel_plan[:]

    cur_total_distance = calculate_round_trip(cur_travel_plan, cities_graph)
    best_total_distance = cur_total_distance

    if PRINT_STATEMENTS:
        print "best travel plan", best_travel_plan
        print "best total distance", best_total_distance

    while (time.time() < end_time):
        # basic_hill_climbing will only return if we have timed out our if
        # we have reached a local minima/maxima
        new_travel_plan, new_total_distance = \
            contingency_hill_climbing(cur_travel_plan,
                                      cities_graph,
                                      end_time,
                                      get_successor)
        if PRINT_STATEMENTS:
            print "new total distance", new_total_distance

        # update our current solution if we have found a better one
        if new_total_distance < best_total_distance:
            cur_total_distance = new_total_distance
            best_travel_plan = new_travel_plan[:]
            best_total_distance = new_total_distance
            if PRINT_STATEMENTS:
                print "best travel plan", best_travel_plan
                print "best total distance", best_total_distance
                print time.time(), end_time

        cur_travel_plan = random.sample(xrange(0, num_cities), num_cities)
        cur_total_distance = calculate_round_trip(cur_travel_plan, cities_graph)

    return best_travel_plan, best_total_distance


def contingency_hill_climbing(travel_plan, cities_graph, end_time, get_successor):
    cur_travel_plan = travel_plan[:]
    cur_total_distance = calculate_round_trip(cur_travel_plan,cities_graph)
    best_neighbor_distance = cur_total_distance
    contingency = False

    # keep looking for better neighbors while there is time and we are not at
    # a local maxima
    while (time.time() < end_time):
        # get a subset of our neighbors as defined by get_succesor
        neighbors = get_successor(cur_travel_plan)

        # evaluate the fitness of each neighbor
        for neighbor_travel_plan in neighbors:
            # get this neighbors fitness
            new_total_distance = calculate_round_trip(neighbor_travel_plan, cities_graph)

            # if this neighbor is the best we've seen update our best_neighbor
            if new_total_distance < best_neighbor_distance:
                best_neighbor_travel_plan = neighbor_travel_plan
                best_neighbor_distance = new_total_distance

        # now that we've seen all our neighbors, check to make sure we have
        # found one better than our current state
        if cur_total_distance <= best_neighbor_distance:
            contingency = True
            if PRINT_STATEMENTS:
                print "local maxima/minima"
            # try another (contingency) neighbor method to make sure we are stuck
            new_travel_plan, new_total_distance = \
                basic_hill_climbing(neighbor_travel_plan,
                                    cities_graph,
                                    end_time,
                                    swap_neighbors)

            # if this contingency stil isn't good enough, give up
            if new_total_distance >= best_neighbor_distance:
                print "\n\n\ncontingency failure\n\n\n"
                return cur_travel_plan, cur_total_distance

            contingency = False
            print "\n\n\ncontingency success\n\n\n"
            best_neighbor_travel_plan = new_travel_plan
            best_neighbor_distance = new_total_distance
            cur_total_distance = best_neighbor_distance
            cur_travel_plan = best_neighbor_travel_plan
            if PRINT_STATEMENTS:
                print "new distance", cur_total_distance
                print "new plan", cur_travel_plan
        else:
            cur_total_distance = best_neighbor_distance
            cur_travel_plan = best_neighbor_travel_plan
            if PRINT_STATEMENTS:
                print "new distance", cur_total_distance
                print "new plan", cur_travel_plan

    print cur_travel_plan, cur_total_distance
    return cur_travel_plan, cur_total_distance


def basic_hill_climbing(travel_plan, cities_graph, end_time, get_successor):
    # get a random starting path
    cur_travel_plan = travel_plan[:]
    cur_total_distance = calculate_round_trip(cur_travel_plan, cities_graph)
    best_neighbor_distance = cur_total_distance

    # keep looking for better neighbors while there is time and we are not at
    # a local maxima
    while (time.time() < end_time):
        # get a subset of our neighbors as defined by get_succesor
        neighbors = get_successor(cur_travel_plan)

        # evaluate the fitness of each neighbor
        for neighbor_travel_plan in neighbors:
            # get this neighbors fitness
            new_total_distance = calculate_round_trip(neighbor_travel_plan,cities_graph)

            # if this neighbor is the best we've seen update our best_neighbor
            if new_total_distance < best_neighbor_distance:
                best_neighbor_travel_plan = neighbor_travel_plan
                best_neighbor_distance = new_total_distance

        # now that we've seen all our neighbors, check to make sure we have
        # found one better than our current state
        if cur_total_distance <= best_neighbor_distance:
            if PRINT_STATEMENTS:
                print "local maxima/minima"
            return cur_travel_plan, cur_total_distance
        else:
            # we've found a better neighbor and must update
            cur_total_distance = best_neighbor_distance
            cur_travel_plan = best_neighbor_travel_plan
            if PRINT_STATEMENTS:
                print "new distance", cur_total_distance
                print "new plan", cur_travel_plan

    return cur_travel_plan, cur_total_distance

def plot_city_coordinates_lineup(cities,best_travel_plan,best_total_distance):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, axisbg="1.0")

    for i in xrange(0,len(best_travel_plan)):
        if i == 0:
            ax.scatter(cities[best_travel_plan[i]].longitude,
                       cities[best_travel_plan[i]].latitude,
                       edgecolors='r')
        else:
            ax.scatter(cities[best_travel_plan[i]].longitude,
                       cities[best_travel_plan[i]].latitude,
                       edgecolors='r')
            ax.plot([cities[best_travel_plan[i-1]].longitude,
                     cities[best_travel_plan[i]].longitude],
                     [cities[best_travel_plan[i-1]].latitude,
                     cities[best_travel_plan[i]].latitude])
    ax.plot([cities[best_travel_plan[-1]].longitude,
             cities[best_travel_plan[0]].longitude],
             [cities[best_travel_plan[-1]].latitude,
             cities[best_travel_plan[0]].latitude])
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Total distance " + str(best_total_distance))
    plt.show()


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

    hill_climb_methods = [#(basic_hill_climbing, "basic_hill_climbing (stops at local minima/maxima)"),
                          #(random_restart_hill_climbing, "random_restart_hill_climbing (when a local minima/maxima is reached, try a new starting point"),
                          (contingency_random_restart_hill_climbing, "contingency_random_restart_hill_climbing (when a local minima/maxima is reached, try another heuristic for a bit. If that doesn't work, try a new starting point")]

    neighbor_heuristics = [#(swap_neighbors, "swap_neighbors (swap a city with it's neighbor to the right)"),
                           #(swap_random_cities, "swap_random_cities (for each city, swap it with a random city)"),
                           (swap_two_random_cities, "swap_two_random_cities (swap one random city with another)")]
    # in seconds
    #run_times = [60], 5*60, 20*60]
    run_times = [120]

    for cities_file in cities_files:
        cities = get_cities_from_file(cities_folder, cities_file)
        num_cities = len(cities)
        cities_graph = cities_graph_from_list(cities)
        starting_travel_plan = random.sample(xrange(0, num_cities), num_cities)

        for hill_climb_method in hill_climb_methods:
            for neighbor_heuristic in neighbor_heuristics:
                for run_time in run_times:
                    print "\n********************************************************************************"
                    print "Using climbing method: ", hill_climb_method[1] \
                        + "\nUsing neightbor heuristic: ", neighbor_heuristic[1] \
                        + "\nRunning for: ", run_time, " seconds"
                    print "********************************************************************************\n"
                    total_run_time = run_time + time.time()
                    best_travel_plan, best_total_distance = \
                        hill_climb_method[0](starting_travel_plan,
                                             cities_graph,
                                             total_run_time,
                                             neighbor_heuristic[0])
                    # graph here?
                    print best_total_distance
                    print best_travel_plan
                    print "\n\n\n\n"
                    plot_city_coordinates_lineup(cities,best_travel_plan,best_total_distance)
