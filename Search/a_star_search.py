"""
    All functions of this file are implemented by me, function prototype of
     solve method was given already as part of the assignment.

    Name: Jitesh Sindhare
    Student ID: U-------
"""

from typing import Callable, List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem
from heuristics import euclidean,manhattan,null
from frontiers import PriorityQueue


def solve(problem: SearchProblem, heuristic: Callable) -> List[str]:
    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """

    multiple_problem=False
    # Remove this line when your solution is implemented
    # *** YOUR CODE HERE ***
    s0 = problem.get_initial_state()
    frontier=PriorityQueue()
    heuristic_value = heuristic(s0, problem)
    # initializing visited state to avoid visiting same state, keep track of visited states
    visited_state = []
    node = s0
    # collect_all is used for backtracking, it contains all the states and its parent which it traversed
    collect_all = {}
    goal_states=[]
    states_followed=[]
    result = node[0]
    list_of_steps = []
    past_cost={}

    future_cost={}
    goal_states.append(s0[1])
    final_cost={}
    if heuristic!=null:
        past_cost[problem.get_initial_state()] = 0
        heuristic_value = heuristic(s0, problem)
        future_cost[s0] = heuristic_value
        final_cost[s0]=past_cost[s0]+future_cost[s0]
    else:
        past_cost[problem.get_initial_state()] = 0
        final_cost[s0] = past_cost[s0]
    frontier.push(s0,final_cost[s0])
    x=True
    while x:


        # checking according to algorithm if frontier is empty then returning false which will result in exiting
        if (frontier.is_empty()):
            x = False
            break
        else:
            node=frontier.pop()
            states_followed.append(node)
            # goal test
            if problem.goal_test(node[0]) :
                x=False
                break

            else:
                # Adding current state to visited states
                # also checking if there is no wall in current node , if yes then skipping this iteration

                if type(node[0]) == int:
                    if problem.get_walls()[node[0]][node[1]]:
                        continue
                    visited_state.append(node)
                elif type(node[1])==tuple :
                    if problem.get_walls()[node[0][0]][node[0][1]]:
                        continue
                    multiple_problem=True
                    visited_state.append(node[0])
                elif type(node[0][1])==tuple:
                    if problem.get_walls()[node[0][0][0]][node[0][0][1]]:
                        continue
                    visited_state.append(node[0])

                elif type(node[1])==str:
                    if problem.get_walls()[node[0][0]][node[0][1]]:
                        continue
                    visited_state.append(node[0])
                #-#  already visited or wall checking ENDS HERE

                # Calling expand function, in this only , I am expanding and checking if nodes are in visited_states
                # and then pushing them inside frontier accordingly
                EXPAND(node, problem, collect_all, visited_state, frontier,past_cost,final_cost,future_cost,heuristic)


    list_of_steps.clear()
    val = 0
    last_parent = node
    list_of_steps.append(node[1])


    # i am seprating backtracking of path by checking if it is a multiple yellow birds problme or not
    if multiple_problem:
        # this loop is mainly for backtracking the path,
        # it runs till value is not equal to initial node,
        # for multiple position problem
        while val != s0:
            for key, values in collect_all.items():
                if last_parent in values:
                    last_parent=key
                    if type(key[1])!=tuple:
                        list_of_steps.append(key[1])
                    val = key
    else:
        #back tracking for single position problem
        while val != s0:
            for key, values in collect_all.items():
                if last_parent in values:
                    last_parent = key
                    if type(key[0]) == int:
                        val = key
                    else:
                        val = key[0]
                        list_of_steps.append(key[1])

    list_of_steps.reverse()
    return list_of_steps


def EXPAND(node, problem, collect_all, visited_state, frontier,past_cost,final_cost,future_cost,heuristic):

    all_nodes = []

    # using this to eliminate an error which was coming due to initial state and next states.
    # , (too many value to unpack error)
    #basically getting state from node and checking if it is multiple position or single position problem
    multiple_position_problem=False
    if type(node[0]) == int :
        state = node
    elif type(node[1])==tuple:
        multiple_position_problem=True
        state=node
    elif type(node[0][1])==tuple:
        multiple_position_problem = True
        state=node[0]
    else:
        state = node[0]

    print('----------------------Node',node)
#getting successor nodes form code below
    for nodes in problem.get_successors(state):
        # checking if successor nodes not in visited_state and not in frontier
        # and those nodes are not walls
        # its for single position problem

        if not multiple_position_problem:
            if not nodes[0] in visited_state:
                if frontier.find(lambda x: x[0] == nodes[0]) == None:

                    if not problem.get_walls()[nodes[0][0]][nodes[0][1]]:
                        #calculating cost of reaching upto this node, i.e. g(n)
                        if heuristic!=null:
                            past_cost[nodes[0]] = nodes[2] + past_cost[state]
                            #claculatiing heuristic value i.e. h(n)
                            heuristic_value = heuristic(nodes[0], problem)
                            # inserting heuristic vlaue of particular node in a dictionary with its state as key
                            future_cost[nodes[0]] = heuristic_value
                            #this is f(n)= g(n) + h(n)
                            final_cost[nodes[0]] = past_cost[nodes[0]] + future_cost[nodes[0]]
                        else:
                            past_cost[nodes[0]] = nodes[2] + past_cost[state]
                            final_cost[nodes[0]] = past_cost[nodes[0]]

                        frontier.push(nodes,final_cost[nodes[0]])
                        # this list below is keeping all nodes from on state which is adding to a list which helps in backtracking
                        all_nodes.append(nodes)
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            # its for multiple position problem
            if not nodes[0] in visited_state:
                if frontier.find(lambda x: x[0][0] == nodes[0][0]) == None:
                    if not problem.get_walls()[nodes[0][0][0]][nodes[0][0][1]]:
                        if heuristic != null:
                            past_cost[nodes[0]] = nodes[2] + past_cost[state]
                            # claculatiing heuristic value i.e. h(n)
                            heuristic_value = heuristic(nodes[0], problem)
                            # inserting heuristic vlaue of particular node in a dictionary with its state as key
                            future_cost[nodes[0]] = heuristic_value
                            # this is f(n)= g(n) + h(n)
                            final_cost[nodes[0]] = past_cost[nodes[0]] + future_cost[nodes[0]]

                        else:
                            #storing state of red ball not consecutive states of left over yellow balls
                            past_cost[nodes[0]] = nodes[2] + past_cost[state]
                            final_cost[nodes[0]] = past_cost[nodes[0]]
                        frontier.push((nodes), final_cost[nodes[0]])
                        # this list below is keeping all nodes from on state which is adding to a list which helps in backtracking

                        #appending all the successor nodes to this
                        all_nodes.append(nodes)
                    else:
                        continue
                else:
                    continue
            else:
                continue

    # adding all nodes to a dictionary with node as key and its successors as values
    # this will be usefull for backtracking
    if len(all_nodes) >= 1:
        collect_all[node] = all_nodes
