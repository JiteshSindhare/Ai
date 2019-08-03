# function prototype was given already as part of the assignment.
# ALl the methods  were implemented by me. EXCEPT last two get methods
"""Heuristics for variable selection and value ordering.

Artificial Intelligence

Student Details
---------------
Student Name: Jitesh Sindhare
Student Number: U-------
Date:   26/04/2018

This is where you need to write your heuristics for variable selection and
value ordering.
"""
from typing import Callable, Dict, List, Optional

from csp import CSP

Assignment = Dict[str, str]


# -----------------------------------------------------------------------------
# Variable Selection Heuristics
# -----------------------------------------------------------------------------


def next_variable_lex(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Select the next variable by lexicographic order.

    Select the next variable from the remaining variables according to
    lexicographic order. We have implemented this one for you.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # gamma.variables is a list of variable names (as strings). See line 43 in
    # csp.py. We consider them in the order they are added in.
    for var in gamma.variables:
        if var not in assignment:
            return var
    return None

# Counts number of unassigned variables a variable has.
def count_unassigned_variables(neighbours, unassigned_variables):
    res=0
    if type(neighbours)==set:
        for n in neighbours:
            if n in unassigned_variables:
                res+=1
            else:
                continue
        return res
    else:
        res=0
        dict=neighbours
        for key,val in dict.items():
            if key in unassigned_variables:
                res+=1
            else:
                continue
        return res


def next_variable_md(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement the most constraining variable (MD) heuristic.

    Choose the variable that won't conflict much with other variables. See
    Lecture 11 for the precise definition. Break ties by lexicographic order.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # *** YOUR CODE HERE ***

    unassigned_variables=[]


    for val in gamma.variables:
        if val not in assignment:
            unassigned_variables.append(val)
    # TYPE OF NEIGHBOURS IS SET -type(gamma.neighbours[unassigned_variables[i]] IS SET

    #---------------------------------CHECKING NEIGHBOURS OF ALL UNASSIGNED VARIABLES-----

    coun_unassigned_variables = -99999999999
    variable_to_send_n=0

    for i in range(len(unassigned_variables)):
        if coun_unassigned_variables<0:
            coun_unassigned_variables=count_unassigned_variables(gamma.neighbours[unassigned_variables[i]], unassigned_variables)
            variable_to_send_n=unassigned_variables[i]
        if i+1<len(unassigned_variables):

            # checking to get the variable which has the higher number of unassigned
            # neighbours because as its said that ,Each variable has a set of neighbouring variables, which it
            # appears in constraints with
            if coun_unassigned_variables<count_unassigned_variables(gamma.neighbours[unassigned_variables[i + 1]], unassigned_variables):
                coun_unassigned_variables=count_unassigned_variables(gamma.neighbours[unassigned_variables[i + 1]], unassigned_variables)
                variable_to_send_n = unassigned_variables[i+1]

            # below elif is the tie-breaking condition, which is done by lexicographical order
            elif coun_unassigned_variables==count_unassigned_variables(gamma.neighbours[unassigned_variables[i + 1]], unassigned_variables):
                variable_to_send_n=next_variable_lex(assignment,gamma)


    # when no more variables to assign left
    if len(unassigned_variables)==0:
        return None
    else:
        return variable_to_send_n

    #------------------------CHECKING NEIGHBOURS OF ALL UNASSIGNED VARIABLES--------ends



def next_variable_mrv(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement the most constrained variable heuristic (MRV).

    Choose the variable with the smallest consistent domain. See Lecture 11 for
    the precise definition. Break ties by lexicographic order.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # *** YOUR CODE HERE ***
    # for list of all unsassigned variables to work with
    unassigned_variables = []

    for val in gamma.variables:
        if val not in assignment:
            unassigned_variables.append(val)
        else:
            continue

# initializing variable for counting and variables
    co_con=0
    variable_return=0
    count_conflicts1=0
    count_conflicts2=0
    for i in range(len(unassigned_variables)):
        temp1=0
        if i==0:
            for d in gamma.current_domains[unassigned_variables[i]]:
                if gamma.count_conflicts(unassigned_variables[i],d)>0:
                    continue
                elif gamma.count_conflicts(unassigned_variables[i],d)==0:
                   temp1+=1
            count_conflicts1=temp1
            variable_return=unassigned_variables[i]
        if i+1<len(unassigned_variables):
            c=0
            for d in gamma.current_domains[unassigned_variables[i+1]]:
                if gamma.count_conflicts(unassigned_variables[i+1],d)>0:
                    continue
                elif gamma.count_conflicts(unassigned_variables[i+1],d)==0:
                   c+=1
            count_conflicts2=c
            if count_conflicts2<count_conflicts1:
                co_con=temp1
                count_conflicts1=count_conflicts2
                variable_return = unassigned_variables[i+1]

                # breaking ties with lexicographical order
            #elif confl==co_con:
            elif count_conflicts2==count_conflicts1:
                variable_return=next_variable_lex(assignment,gamma)
    #print('v',con_var)
    if len(unassigned_variables)==0:
        return None
    else:
        return variable_return


    #raise NotImplementedError("Error: MRV heuristic not implemented yet!")


def next_variable_md_mrv(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement MD heuristic, breaking ties with MRV.

    Choose the variable that won't conflict much with other variables. If there
    is a tie, choose the variable with the smallest consistent domain. See
    Lecture 11 for the precise definition.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # *** YOUR CODE HERE ***
    # initializing list of unassigned variables
    unassigned_variables=[]
    # getting lsit of all unassigned variables
    for val in gamma.variables:
        if val not in assignment:
            unassigned_variables.append(val)

    #---------------------------------CHECKING NEIGHBOURS OF ALL UNASSIGNED VARIABLES
    coun_unassigned_neighbours = -9999999999
    variable_to_send_n=0

    for i in range(len(unassigned_variables)):
        if coun_unassigned_neighbours<0:
            coun_unassigned_neighbours=count_unassigned_variables(gamma.neighbours[unassigned_variables[i]], unassigned_variables)
            variable_to_send_n=unassigned_variables[i]
        if i+1<len(unassigned_variables):
            if coun_unassigned_neighbours<count_unassigned_variables(gamma.neighbours[unassigned_variables[i + 1]], unassigned_variables):
                coun_unassigned_neighbours=count_unassigned_variables(gamma.neighbours[unassigned_variables[i + 1]], unassigned_variables)
                variable_to_send_n = unassigned_variables[i+1]

                # breaking ties with mrv , as directed
            elif coun_unassigned_neighbours==count_unassigned_variables(gamma.neighbours[unassigned_variables[i + 1]], unassigned_variables):
                variable_to_send_n=next_variable_mrv(assignment,gamma)

    if len(unassigned_variables)==0:
        return None
    else:
        return variable_to_send_n


def next_variable_mrv_md(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement MRV heuristic, breaking ties with MD.

    Choose the variable with the smallest consistent domain. If there is a tie,
    choose the variable that won't conflict much with other variables. See
    Lecture 11 for the precise definition.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # *** YOUR CODE HERE ***

    # for list of all unsassigned variables to work with
    unassigned_variables = []

    for val in gamma.variables:
        if val not in assignment:
            unassigned_variables.append(val)
        else:
            continue

    # initializing variable for counting and variables
    co_con = 0
    variable_to_return = 0
    count_conflicts1 = 0
    count_conflicts2 = 0
    for i in range(len(unassigned_variables)):
        temp1 = 0
        if i == 0:
            for d in gamma.current_domains[unassigned_variables[i]]:
                if gamma.count_conflicts(unassigned_variables[i], d) > 0:
                    continue
                elif gamma.count_conflicts(unassigned_variables[i], d) == 0:
                    temp1 += 1
            count_conflicts1 = temp1
            variable_to_return = unassigned_variables[i]
        if i + 1 < len(unassigned_variables):
            c = 0
            for d in gamma.current_domains[unassigned_variables[i + 1]]:
                if gamma.count_conflicts(unassigned_variables[i + 1], d) > 0:
                    continue
                elif gamma.count_conflicts(unassigned_variables[i + 1], d) == 0:
                    c += 1
            count_conflicts2 = c
            if count_conflicts2 < count_conflicts1:
                co_con = temp1
                count_conflicts1 = count_conflicts2
                variable_to_return = unassigned_variables[i + 1]

                # breaking ties with md
            elif count_conflicts2 == count_conflicts1:
                variable_to_return = next_variable_md(assignment, gamma)

    if len(unassigned_variables) == 0:
        return None
    else:
        return variable_to_return


# -----------------------------------------------------------------------------
# Value Ordering Heuristics
# -----------------------------------------------------------------------------


def value_ordering_lex(var: str, assignment: Assignment, gamma: CSP) -> List[str]:
    """Order the values based on lexicographic order.

    In this heuristic, variable values are ordered in lexicographic order. We
    have implemented this heuristic for you. We make use of the attribute
    `gamma.current_domains` to be useful. This is a dictionary that maps a
    variable name (a string) to a set of values (a set of strings) in that
    variable's current domain.

    Parameters
    ----------
    var : str
        The name of the variable which we want to assign a value.
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    values : List[str]
        A list the values (represented a strings) in the current domain of the
        variable, sorted according to this heuristic.

    """
    # We need to explicitly convert a set to a list.

    return list(gamma.current_domains[var])


def value_ordering_lcvf(var: str, assignment: Assignment, gamma: CSP) -> List[str]:
    """Order the values based on the Least Constraining Value heuristic.

    This heuristic returns values in order of how constraining they are. It
    prefers the value that rules out the fewest choices for the neighbouring
    variables in the constraint graph. In other words,  it prefers values which
    remove the fewest elements from the current domains of their neighbouring
    variables.

    See Lecture 11 for the precise definition. You might find the attribute
    `gamma.current_domains` to be useful. This is a dictionary that maps a
    variable name (a string) to a set of values (a set of strings) in that
    variable's current domain.

    Parameters
    ----------
    var : str
        The name of the variable which we want to assign a value.
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    values : List[str]
        All the values in  the current domain of the variable, sorted according
        to this heuristic.

    """

    result=[]
    # *** YOUR CODE HERE ***
    last_val=[]
    for d in gamma.current_domains[var]:
        #since we have to find value which is least constraint, so first getting number of violated constraints
        # and then accordingly saved and sorted
        c=gamma.get_violated_constraints(var,d) # its type is set

        if len(last_val)>0:
            if last_val[-1]>len(c):
                l=last_val[-1]
                last_val.remove(l)
                last_val.append(len(c))
                last_val.append(l)
                r=result[-1]
                result.remove(r)
                result.append(d)
                result.append(r)
            elif last_val[-1]<=len(c):
                last_val.append(len(c))
                result.append(d)
        else:
            last_val.append(len(c))
            result.append(d)

    #sorting the resulting list according to heuristic with best value of domain first
    for k in range(len(last_val)):
        for i in range(len(last_val)):
            if i+1<len(last_val):
                if last_val[i+1]<last_val[i]:
                    a=last_val[i+1]
                    b=last_val[i]
                    last_val[i]=a
                    last_val[i+1] = b
                    c=result[i+1]
                    d = result[i]
                    result[i]=c
                    result[i+1]=d

    #result.reverse() # since it should be minimum heuristic so reversing is not needed.
    return result


# -------------------------------------------------------------------------------
# Functions used by the system to select from the above heuristics for the search
# You do not need to look any further.
# -------------------------------------------------------------------------------

def get_variable_selection_function(variable_heuristic: str) -> Callable:
    """Return the appropriate variable selection function."""
    if variable_heuristic == "lex":
        return next_variable_lex
    if variable_heuristic == "md":
        return next_variable_md
    if variable_heuristic == "mrv":
        return next_variable_mrv
    if variable_heuristic == "md-mrv":
        return next_variable_md_mrv
    if variable_heuristic == "mrv-md":
        return next_variable_mrv_md

    raise ValueError(f"Error: the variable selection heuristic "
                     f"'{variable_heuristic}' is not supported")


def get_value_ordering_function(value_heuristic: str) -> Callable:
    """Return the appropriate value ordering function."""
    if value_heuristic == "lex":
        return value_ordering_lex
    if value_heuristic == "lcvf":
        return value_ordering_lcvf

    raise ValueError(f"Error: the value selection heuristic "
                     f"'{value_heuristic}' is not supported")
