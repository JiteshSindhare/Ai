# Function prototype f forward_checkign and arc_consistent was given already as part of the assignment.
# ALl the methods was implemented by me. EXCEPT last two(no_inference, get).
"""Inference functions used with backtracking search.

Student Details
---------------
Student Name:   Jitesh Sindhare
Student Number: U-------
Date:   9/05/2018
"""

import collections,copy
from typing import Callable, Dict, List, Optional, Tuple

from csp import CSP

Assignment = Dict[str, str]
Pruned = List[Tuple[str, str]]


def forward_checking(var: str, assignment: Assignment, gamma: CSP) -> Optional[Tuple[Pruned, Assignment]]:
    """Implement the forward checking inference procedure.

    Parameters
    ----------
    var : str
        The name of the variable which has just been assigned.
    assignment : Dict[str, str]
        A Python dictionary of the current assignment. The dictionary maps
        variable names to values. The function cannot change anything in
        `assignment`.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution. The function cannot change
        anything in `gamma`.

    Returns
    -------
    (pruned_list, new_assignment) : Optional[Tuple[Pruned, Assignment]]
        In the case that the algorithm detects a conflict, the assignment and
        CSP should remain unchanged and the function should return None.

        Otherwise, the algorithm should return a pair of (pruned_list,
        new_assignments) where:
            - 'pruned_list' is a list of (variable, value) pairs that will be
               pruned out of the domains of the variables in the problem. Think
               of this as the "edits" that are required to be done on the
               variable domains.
            - 'new_assignments' is a dictionary containing new assignments made
               by the inference procedure. The dictionary maps variable names
               to values. It contains any assignment resulting from reducing the
               domain of a variable to be a singleton. If no domain is reduced
               in such a way, it needs to be an empty dictionary.

    """
    # *** YOUR CODE HERE ***
    unassigned_variable=[]
    pruned_list=[]
    new_assignment={}
    for v in gamma.variables:
        if v not in assignment:
            unassigned_variable.append(v)

    assigned_value=assignment[var]

    # checking if there is conflict then to return None
    if gamma.count_conflicts(var,assigned_value)>0:
        return None
    else:
        #checking all neighbours
        for n in gamma.neighbours[var]:
            if n in unassigned_variable:
                cur_dom=gamma.current_domains[n]
                # if assigned value is in domains of neighbours
                if assigned_value in cur_dom:
                    pruned_list.append((n,assigned_value))
                    # checking if aside from the current value any other value is thr in current
                    #domain of neighour so that if it is potential singleton
                    if len(cur_dom)==2:
                        a=(cur_dom - set(assigned_value)).pop()

                        new_assignment[n] = a
                        # checking if there is conflict in this singleton value then returning None
                        if gamma.count_conflicts(n,a)>0:
                            return None
                    elif len(cur_dom)==1:
                        return None

                # remove this else if it does not make much different.
                else:
                    if len(gamma.current_domains[n]) == 1:
                        new_assignment[n]=gamma.current_domains[n]



        return (pruned_list,new_assignment)



def REVISE(gamma:CSP,elem,domains,pruned_list,
           unassigned_variables,new_assignment):

    x_i=elem[0]
    x_j=elem[1]
    confl=False
    D_i=domains[x_i].copy()
    for x in D_i.copy():
        if confl :
            break
        check=0
        # this contains conflict value of of x_j i.e. neighbour of x_i
        conflict_value=gamma.conflicts[(x_i,x)][x_j]
        # subtracting that conflict value from domain of x_j which is neighbour
        check=domains[x_j].difference(conflict_value)
        # if after subtraction from domain of x_j no value left that means there is no value to satisfy constraint
        # between x_i and x_j when x_i=x so we remove that value 'x' from domain of x_i
        if len(check)==0:
            domains[x_i].remove(x)
            if (x_i, x) not in pruned_list:
                pruned_list.append((x_i, x))
        else:
            continue

        # checking if there is only 1 value left in domain of x_i then making it assignment of that variable
        xy = domains[x_i]
        if len(xy) == 1:
            val = xy.pop()
            new_assignment[x_i] = val
            domains[x_i] = set(val)
            if x_i in unassigned_variables:
                unassigned_variables.remove(x_i)
            # checking if this singleton assignment is a conflict then returning True which ultimately return None
            if gamma.count_conflicts(x_i, val) > 0:
                confl = True
                #break
                continue
            else:
                break
#                continue

    if confl:
        return None
    else:
        return True

def arc_consistency(var: Optional[str], assignment: Assignment, gamma: CSP) -> Optional[Tuple[Pruned, Assignment]]:
    """Implement the AC-3 inference procedure.

    Parameters
    ----------
    var : Optional[str]
        The name of the variable which has just been assigned. In the case that
        AC-3 is used for preprocessing, `var` will be `None`.
    assignment : Dict[str, str]
        A Python dictionary of the current assignment. The dictionary maps
        variable names to values. The function cannot change anything in
        `assignment`.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution. The function cannot change
        anything in `gamma`.

    Returns
    -------
    (pruned_list, new_assignment) : Optional[Tuple[Pruned, Assignment]]
        In the case that the algorithm detects a conflict, the assignment and
        CSP should remain unchanged and the function should return None.

        Otherwise, the algorithm should return a pair of (pruned_list,
        new_assignments) where:
            - 'pruned_list' is a list of (variable, value) pairs that will be
               pruned out of the domains of the variables in the problem. Think
               of this as the "edits" that are required to be done on the
               variable domains.
            - 'new_assignments' is a dictionary containing new assignments made
               by the inference procedure. The dictionary maps variable names
               to values. It contains any assignment resulting from reducing the
               domain of a variable to be a singleton. If no domain is reduced
               in such a way, it needs to be an empty dictionary.

    """
    # *** YOUR CODE HERE ***

    if not var==None:
        if gamma.count_conflicts(var,assignment[var])>0:
            return None

    unassigned_variables=[]
    # initializing queue
    queue=collections.deque()
    #copying domains and assignments , since its usefull for REVISE function
    # deepcopy because it replicates dictionary , shallow is like it makes references/pointer of a dictionary
    domains=copy.deepcopy(gamma.current_domains)

    # initializing variables to return
    new_assignment={}
    pruned_list=[]

    for vars in gamma.variables:
        if vars not in assignment:
            unassigned_variables.append(vars)

    if len(unassigned_variables)==0:
        return None

# i am adding assignned variables normally because i want them to be processed first so that they will make
# the current domains of others what it should be, and since unassigned variable ones are appendleft so by the time they will
# be processed their current domains will be shortened as to what they should be.

    # separated queue for when var is None and not None to make it more time efficient
    if var!=None:
        for n in gamma.neighbours[var]:
            if n in unassigned_variables:
                queue.appendleft((var, n))
                queue.appendleft((n, var))
    else:
        for a in unassigned_variables:
            for n in gamma.neighbours[a]:
                if n in unassigned_variables:
                    queue.appendleft((a,n))
                elif n in assignment:
                    queue.append((a,n))


    previous_domain=0
    # Below is the while loop to run until queue is empty acc. to algo.
    while len(queue)>0:
        elem=queue.pop()
        previous_domain = domains[elem[0]]
        r=REVISE(gamma,elem,domains,pruned_list,
                 unassigned_variables,new_assignment)
        # Below is the case when it is getting conflicts in newly assigned variables
        if r==None:
            return None
        # to check if domain changed
        if previous_domain!=domains[elem[0]]:
            for n in gamma.neighbours[elem[0]]:
                if n==elem[0]:
                    continue
                if n in unassigned_variables:
                    queue.appendleft((n,elem[0]))

    return tuple((pruned_list,new_assignment))


# -------------------------------------------------------------------------------
# A function use to get the correct inference method for the search
# You do not need to touch this.
# -------------------------------------------------------------------------------

def get_inference_function(inference_type: str) -> Callable:
    """Return the function that does the specified inference."""
    if inference_type == "forward":
        return forward_checking
    if inference_type == "arc":
        return arc_consistency

    # If no inference is specified, we simply do nothing.
    def no_inference(var, assignment, csp):
        return [], {}

    return no_inference

