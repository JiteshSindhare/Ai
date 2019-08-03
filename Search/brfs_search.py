"""
    All functions of this file are implemented by me, function prototypes of solve method
    was given by tutors of the course.

    Name: Jitesh Sindhare
    Student ID: U-------
"""
# Reference - lambda function - https://medium.com/@happymishra66/lambda-map-and-filter-in-python-4935f248593
from typing import List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem
import search_strategies
from frontiers import Queue
from frontiers import PriorityQueue

def solve(problem: SearchProblem) -> List[str]:
    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """
    #initializing initial state
    s0 = problem.get_initial_state()


    frontier = Queue()
    #initiale_node
    # initializing visited state to avoid visiting same state, keep track of visited states
    visited_state=[]
    node=s0
    # collect_all is used for backtracking, it contains all the states and its parent which it traversed
    collect_all={}
    frontier.push(s0)
    result=node[0]
    list_of_steps=[]

    while((not frontier.is_empty()) or  problem.goal_test(result)):
        #checking according to algorithm if frontier is empty then returning false which will result in exiting
        if (frontier.is_empty()):
            x=False
            break
        else:
            # else removes First element from FRONTIER according to FIFO
            node=frontier.pop()

            if problem.goal_test(node[0]):
                break
            else:
               #Adding current state to visited states
               #also checking if there is no wall in current node , if yes then skipping this iteration
                if type(node[0])==int:
                    if  problem.get_walls()[node[0]][node[1]]:
                        continue
                    visited_state.append(node)
                else:
                    if  problem.get_walls()[node[0][0]][node[0][1]]:
                        continue
                    visited_state.append(node[0])

                # checking if current state is already visited or if it is a wall ENDS HERE
            #Calling expand function, in this only , I am expanding and checking if nodes are in visited_states
            # and then pushing them inside frontier accordingly
                EXPAND(node, problem,collect_all,visited_state,frontier)

    list_of_steps.clear()
    #-------------------------
    val=0
    last_parent = node
    list_of_steps.append(node[1])

    # this loop is mainly for backtracking the path,
    # it runs till value is not equal to initial node,
    # here i am checking all values and then taking its keys. and its actions are appended to return at last
    while val!=s0:
        for key,values in collect_all.items():
            if last_parent in values:
                last_parent=key
                if type(key[0])==int:
                    val=key
                else:
                    val=key[0]
                    list_of_steps.append(key[1])

    list_of_steps.reverse()
    #delete below printing line while submitting
    print('collect all has',collect_all)
    return list_of_steps


def EXPAND(node, problem,collect_all,visited_state,frontier):

    all_nodes=[]

#using this to eliminate an error which was coming due to initial state and next states., (too many value to unpack error)
    if type(node[0])==tuple:
        state=node[0]
    else:
        state=node

    for nodes in problem.get_successors(state):
        #initializing new node sn using function from SearchNode
#checking if nodes not in visited_state and not in frontier
        if nodes[0] not in visited_state:
            if frontier.find(lambda x:x[0]==nodes[0])==None:
                frontier.push(nodes)
                all_nodes.append(nodes)
            else:
                continue
        else:
            continue

    # adding all nodes to a dictionary with node as key and its successors as values
    # this will be usefull for backtracking
    if len(all_nodes)>=1:
        #collect_all[node]=successors
        collect_all[node]=all_nodes

