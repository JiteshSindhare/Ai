# function prototype was given already as part of the assignment. rest is done by me
""" File name:   disease_scenario.py
    Author:         Jitesh Sindhare/ UNI-ID- -------
    Date:           5/03/2019
    Description: This file represents a scenario simulating the spread of an
                 infectious disease around Australia. It should be
                 implemented for Part 1 of Exercise 4 of Assignment 0.

                 See the lab notes for a description of its contents.
"""
import copy

# this does not work in 3.6 or in windows if this classs DiseaseScenario does not extend "object"
class DiseaseScenario(object):
    def __init__(self):
        """ YOUR CODE HERE. """
        self.threshold = float(0)
        self.growth = float(0)
        self.spread = float(0)
        self.location = ''
        self.locations = []
        self.disease = {}
        self.conn = {}
        self.prev = {}
        #  variable "self.prev" is created to keep track of disease in previous iteration

    def read_scenario_file(self, path_to_scenario_file):
        """ Checking first word from file and according redirecting things to respective variable using if/else """
        try:
            with open(path_to_scenario_file) as screnario_file:
                for line in screnario_file:
                    words = line.split()
                    if words[0] == 'threshold':
                        self.threshold = float(words[1])
                    elif words[0] == 'growth':
                        self.growth = float(words[1])
                    elif words[0] == 'spread':
                        self.spread = float(words[1])
                    elif words[0] == 'start':  # it is location of agent
                        self.location = str(words[1])
                    elif words[0] == 'location':

                        self.locations.append(str(words[1]))
                    elif words[0] == 'disease':
                        self.disease[words[1]] = float(words[2])

                    elif words[0] == 'conn':

                        if (words[1] in self.conn.keys()):

                            self.conn[words[1]].update(words[2].split())
                            if (words[2] in self.conn.keys()):
                                self.conn[words[2]].update(words[1].split())
                            else:
                                self.conn[words[2]] = set(words[1].split())
                        else:
                            self.conn[words[1]] = set(words[2].split())
                            if (words[2] in self.conn.keys()):
                                self.conn[words[2]].update(words[1].split())
                            else:
                                self.conn[words[2]] = set(words[1].split())
                for i in range(len(self.locations)):
                    if self.locations[i] not in self.disease.keys():
                        self.disease[self.locations[i]] = 0
                # Knowledge of how to copy one dictionary to another came form here
                #   https://stackoverflow.com/questions/2465921/how-to-copy-a-dictionary-and-only-edit-the-copy
                # The knowledge that I should use deep copy or shallow copy came from here
                #   https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/

                self.prev = copy.deepcopy(self.disease)
                return True
        except IOError as e:
            return False



    def valid_moves(self):
        """ Checking the connections from the conn variable from . """
        a = []
        a.append(self.location)
        if self.location in self.conn.keys():
            for values in self.conn[self.location]:
                a.append(values)
            return a
        else:
            return a.append(self.location)


    def move(self, loc):
        """ Checking if the agent can be moved to the locatio ngiven in the function, If yes then updating the location of agent
        else raising a valueError as said in the description. """
        if loc in self.conn[self.location]:
            self.location = loc
            self.disease[loc] = 0
        else:
            raise ValueError('There is no connecting road between {} and {}'.format(self.location, loc))


    """ In the function below , I am calculating the disease as explained in the description, and for that I am checking if 
    the agent is not present in that position, For taking the disease value of any location in nth time which is used in n+1 iteration
     for its neighbour I am saving/copying the disease in nth iteration of that location in dictionary."""
    def spread_disease(self):
        """ YOUR CODE HERE. """

        for keys in self.disease.keys():
            if keys != self.location:

                grow = float(self.growth) + int(1)

                self.disease[keys] = self.disease[keys] * grow
                # got idea about how to get elements of a set form here -https://stackoverflow.com/questions/59825/how-to-retrieve-an-element-from-a-set-without-removing-it

                for i in self.conn[keys]:
                    if i != self.location and self.prev[i] >= self.threshold:
                        self.disease[keys] = (self.disease[keys]) + (self.prev[i] * self.spread)

            elif keys == self.location:
                self.disease[keys] = 0
        self.prev = copy.deepcopy(self.disease)
        # print('-------------------------------------------')

