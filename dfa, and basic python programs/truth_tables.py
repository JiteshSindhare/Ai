# -*- coding: utf-8 -*-
# function prototype was given already as part of the assignment. rest is done by me
""" File name:   truth_tables.py
    Author:      <Jitesh Sindhare>
    Date:        <2/3/2019>
    Description: This file defines a number of functions which implement Boolean
                 expressions.

                 It also defines a function to generate and print truth tables
                 using these functions.

                 It should be implemented for Exercise 2 of Assignment 0.

                 See the assignment notes for a description of its contents.
"""


def boolean_fn1(a, b, c):
    """ Return the truth value of (a ∨ b) → (-a ∧ -b) """
    # YOUR CODE HERE
    if ( not (a or b )  or ( ( not a ) and ( not b ) ) ):
        return True
    else:
        return False


def boolean_fn2(a, b, c):
    """ Return the truth value of (a ∧ b) ∨ (-a ∧ -b) """
    # YOUR CODE HERE
    if( (a and b ) or ( (not a) and (not b) ) ):
        return True
    else:
        return False

def boolean_fn3(a, b, c):
    """ Return the truth value of ((c → a) ∧ (a ∧ -b)) ∨ (-a ∧ b) """
    # YOUR CODE HERE
    if ( ( not c or a ) and ( a and ( not b ) ) or ( ( not a ) and b ) ):
        return True
    else:
        return False

def draw_truth_table(boolean_fn):
    """ This function prints a truth table for the given boolean function.
        It is assumed that the supplied function has three arguments.

        ((bool, bool, bool) -> bool) -> None

        If your function is working correctly, your console output should look
        like this:

        >>> from truth_tables import *
        >>> draw_truth_table(boolean_fn1)

        a     b     c     res
        -----------------------
        False False False True
        False False True  True
        False True  False False
        False True  True  False
        True  False False False
        True  False True  False
        True  True  False False
        True  True  True  False
    """

#idea of how to format/align it came from here
# https://stackoverflow.com/questions/9535954/printing-lists-as-tabular-data#
    print('%-5s %-5s %-5s %-5s'%("a","b","c","res"))
    print('-----------------------')
    print('%-5s %-5s %-5s %-5s' % ("False", "False","False",boolean_fn(0, 0, 0)))
    print('%-5s %-5s %-5s %-5s' % ( "False","False","True",boolean_fn(0, 0, 1)   )  )
    print('%-5s %-5s %-5s %-5s' % ( "False","True","False", boolean_fn(0, 1, 0)  ) )
    print('%-5s %-5s %-5s %-5s' % ( "False", "True", "True", boolean_fn(0, 1, 1)    )   )
    print('%-5s %-5s %-5s %-5s' % ( "True","False","False", boolean_fn(1, 0, 0) )   )
    print('%-5s %-5s %-5s %-5s' % ( "True","False","True",boolean_fn(1, 0, 1)   )   )
    print('%-5s %-5s %-5s %-5s' % ("True","True","False",boolean_fn(1, 1, 0)   )  )
    print('%-5s %-5s %-5s %-5s' % ( "True","True","True",boolean_fn(1, 1, 1)    )   )

