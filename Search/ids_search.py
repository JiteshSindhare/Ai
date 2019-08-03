"""
    All functions of this file are implemented by me, function prototype of solve method
    was given already as part of the assignment.


    Name:   Jitesh Sindhare
    Student ID: U-------
"""

from typing import List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem
from frontiers import Stack


parent_and_child={}
def solve(problem: SearchProblem) -> List[str]:
    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """

    # Remove this line when you have implemented Iterative Deepening Depth First Search
    # initializing initial state

    # initiale_node
    # initializing visited state to avoid visiting same state, keep track of visited states
    #final_node=0
    result=0
    actions=[]
    import sys

    sys.setrecursionlimit(20000)
    # collect_all is used for backtracking, it contains all the states and its parent which it traversed
    for depth in range(0,9999999999999):
        result=DEPTH_LIMITED_SEARCH(problem,depth)

        if not result=='cut_off':
            print('limit',depth)
            break


    val1=0
    actions.append(result[1])



    while val1 != problem.get_initial_state():
        for key,values in parent_and_child.items():

            for i in range(len(values)):
                if result in values or result==values:
                    val1=key
                    result=key

                    if type(key[0])==int:
                        None
                    else:
                        actions.append(key[1])

    actions.reverse()
    return actions

def DEPTH_LIMITED_SEARCH(problem,limit):

    DEPTH={}
    past_cost={}
    DEPTH[problem.get_initial_state()]=0
    visited_state=[]
    frontier=Stack()

    list12=[]
    past_cost[problem.get_initial_state()]=0

    print('limit',limit)
    return RECURSIVE_DLS(problem.get_initial_state(),problem,limit,visited_state,DEPTH,frontier,list12,past_cost)
    # return line is still left - SEE ALGO

def RECURSIVE_DLS(node,problem,limit,visited_state,DEPTH,frontier,list12,past_cost):# return line is still left - SEE ALGO

    list12.clear()
    cut_off_occured=False
    if type(node[0])==int:
        state=node
    else:
        state=node[0]
#checking if current state is goal state
    if problem.goal_test(state):
        return node
# checking if DEPTH of current node is equal to limit then cutoff
    elif DEPTH[state]==limit:
        return 'cut_off'
    else:
        if type(node[0]) == int:
            state=node
        else:
            state = node[0]
            #getting successors of state
        for successor in problem.get_successors(state):
            # checking so tht it does not end up in self loop
            if successor[0] in DEPTH:
                if DEPTH[successor[0]]<(DEPTH[state]) or successor[0]==problem.get_initial_state():
                    continue

            else:
                # keeping list of last 2 expanded state
                if state not in visited_state :
                    if len(visited_state)>(2):
                        visited_state.pop(0)
                        visited_state.append(state)
                    else:
                        visited_state.append(state)



                #keeping list of all parents and child keys
                if node in parent_and_child:
                    check=list(parent_and_child[node])
                    if successor not in check:
                        l=[]
                        l.append(parent_and_child[node])
                        l.append(successor)
                        parent_and_child[node]=l
                else:
                    parent_and_child[node] = successor


            # keeping track of depths of all the nodes
            if successor[0] not in DEPTH:
                DEPTH[successor[0]] = DEPTH[state] + 1
#recursive calling acc. to algo
            resul=RECURSIVE_DLS(successor,problem,limit,visited_state,DEPTH,frontier,list12,past_cost)
            if resul=='cut_off':
                cut_off_occured=True
            elif not resul=='failure':
                return resul
        if cut_off_occured:
            return 'cut_off'
        else:
            return 'failure'

#python red_bird.py -l search_layouts/anuSearch.lay -p SearchAgent -a fn=ids
