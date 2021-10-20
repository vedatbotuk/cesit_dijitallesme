# Python program to print all paths from a source to destination.

from collections import defaultdict


# This class represents a directed graph
# using adjacency list representation
class Graph:

    def __init__(self):

        kapali = 1
        stop = 2
        start = 3
        counter = 4
        ariza = 5
        ayar = 6
        bobin = 7
        cozgu = 8
        reset = 9

        # Create a graph given in the above diagram
        vertices = 26

        # No. of vertices
        self.V = vertices
        self.pp = []
        self.p = ''

        # default dictionary to store graph
        self.graph = defaultdict(list)

        self.__add_edge(kapali, stop)

        self.__add_edge(stop, kapali)
        self.__add_edge(stop, start)
        self.__add_edge(stop, ariza)
        self.__add_edge(stop, ayar)
        self.__add_edge(stop, bobin)
        self.__add_edge(stop, cozgu)
        self.__add_edge(stop, reset)

        self.__add_edge(reset, stop)

        self.__add_edge(start, stop)
        self.__add_edge(start, counter)

        self.__add_edge(counter, start)

        self.__add_edge(ariza, stop)
        self.__add_edge(ariza, ayar)
        self.__add_edge(ariza, bobin)
        self.__add_edge(ariza, cozgu)

        self.__add_edge(ayar, stop)
        self.__add_edge(ayar, ariza)
        self.__add_edge(ayar, bobin)
        self.__add_edge(ayar, cozgu)

        self.__add_edge(bobin, stop)
        self.__add_edge(bobin, ariza)
        self.__add_edge(bobin, ayar)
        self.__add_edge(bobin, cozgu)

        self.__add_edge(cozgu, stop)
        self.__add_edge(cozgu, ariza)
        self.__add_edge(cozgu, bobin)
        self.__add_edge(cozgu, ayar)

    # function to add an edge to graph
    def __add_edge(self, u, v):
        self.graph[u].append(v)

    '''A recursive function to print all paths from 'u' to 'd'.
    visited[] keeps track of vertices in current path.
    path[] stores actual vertices and path_index is current
    index in path[]'''

    def print_all_paths_util(self, u, d, visited, path):

        # Mark the current node as visited and store in path

        visited[u] = True
        if u == 1:
            self.p = 'kapali'
        elif u == 2:
            self.p = 'stop'
        elif u == 3:
            self.p = 'start'
        elif u == 4:
            self.p = 'counter'
        elif u == 5:
            self.p = 'ariza'
        elif u == 6:
            self.p = 'ayar'
        elif u == 7:
            self.p = 'bobin'
        elif u == 8:
            self.p = 'cozgu'

        path.append(self.p)

        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            # print(path)
            self.pp.append(path[0:])
        # print(path[0:2])
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.graph[u]:
                if not visited[i]:
                    self.print_all_paths_util(i, d, visited, path)

        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u] = False

    # Prints all paths from 's' to 'd'
    def print_all_paths(self, s, d):

        # Mark all the vertices as not visited
        visited = [False] * self.V

        # Create an array to store paths
        path = []
        self.pp = []

        # Call the recursive helper function to print all paths
        self.print_all_paths_util(s, d, visited, path)

        return self.pp
