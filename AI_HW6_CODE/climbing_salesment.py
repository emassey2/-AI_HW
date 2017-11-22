#!/usr/bin/python

import re
import math
import random

DEBUG_LEVEL = 2

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
    cities_graph = [[-1 for x in xrange(num_cols)] for y in xrange(num_rows)]

    count = 0
    for i in xrange(num_cols):
        for j in xrange(num_rows):
            if cities[i] != cities[j]:
                cities_graph[i][j] = get_cities_distance(cities[i], cities[j])
                count += 1

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
