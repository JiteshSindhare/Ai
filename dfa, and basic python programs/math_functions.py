# function prototype was given already as part of the assignment. rest is done by me
""" File name:   math_functions.py
    Author:      <Jitesh Sindhare>
    Date:        <1/3/2019>
    Description: This file defines a set of variables and simple functions.

                 It should be implemented for Exercise 1 of Assignment 0.

                 See the assignment notes for a description of its contents.
"""
import math
ln_e =math.log(math.e)  # YOUR CODE HERE

twenty_radians =math.radians(20)  # YOUR CODE HERE


def quotient_ceil(numerator, denominator):
    """ This code is returning ceiling(rounded up) of division of numerator  by denominator"""
    return int(math.ceil(numerator/denominator))


def quotient_floor(numerator, denominator):
    """ This code is returning floor(rounded down) of division of numerator  by denominator """
    return  int(math.floor(numerator/denominator))


def manhattan(x1, y1, x2, y2):
    """ This function is calculating manhattan distance between two points (x1,y1,) and (x2,y2) """
    return int(math.fmod(x1,x2)+math.fmod(y1,y2))
