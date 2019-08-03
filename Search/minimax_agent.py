# minimax_agent.py
# --------------
"""
   Maximize and Minimize methods are done by me, rest was given already as part of the assignment.
"""

from typing import Tuple

from agents import Agent
from game_engine.actions import Directions
from search_problems import AdversarialSearchProblem

Position = Tuple[int, int]
Positions = Tuple[Position]
State = Tuple[int, Position, Position, Positions, float, float]


class MinimaxAgent(Agent):
    """ The agent you will implement to compete with the black bird to try and
        save as many yellow birds as possible. """

    def __init__(self, max_player, depth="2"):
        """ Make a new Adversarial agent with the optional depth argument.
        """
        self.max_player = max_player
        self.depth = int(depth)
        self.max_util=''
        self.visted=[]
        self.m_state=''

    def evaluation(self, problem: AdversarialSearchProblem, state: State) -> float:
        """
            (MinimaxAgent, AdversarialSearchProblem,
                (int, (int, int), (int, int), ((int, int)), number, number))
                    -> number
        """
        player, red_pos, black_pos, yellow_birds, score, yb_score = state
        # *** YOUR CODE GOES HERE ***

        return score

    def maximize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha=float('-inf'), beta=float('inf')) -> Tuple[float, str]:
        """ This method should return a pair (max_utility, max_action).
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.
        """

        if problem.terminal_test(state) or current_depth==self.depth:
            action=Directions.STOP
            return tuple((problem.utility(state),action))
        else:
            action = Directions.STOP
            v=(-999999999999999)
            v2 = 0
            action2=''
            #v=-float("inf")
            for successor,action1,cost in problem.get_successors(state):
                c=self.minimize(problem, successor, current_depth + 1,alpha,beta)
                v1 = max(v,c)

#                v=v1
                if v1>v:
                    v2=v1
                    action2=action1

                    if v2>=beta:
                        v=v2
                        action = action2
                        return tuple((v,action))
                    else:
                        v=v1
                        action=action1
                        alpha = max(alpha, v2)
            return tuple((v2,action))
        #raise_not_defined()  # Remove this line once you finished your implementation

        # *** YOUR CODE GOES HERE ***

    def minimize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha=float('-inf'), beta=float('inf')) -> float:
        """ This function should just return the minimum utility.
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.
        """

        if problem.terminal_test(state) or current_depth==self.depth:
            #return problem.utility(state)
            return problem.utility(state)
        else:
            #v=9999999999999
            v=float("inf")
            for successor,action1,cost in problem.get_successors(state):

                player, red_pos, black_pos, yellow_birds, score, yb_score = successor
                a, b = self.maximize(problem, successor, current_depth+1,alpha,beta)
                #print('a',a,'b',b,'v',v)
                v1 = min(v,a)
                #v = v1
                v=v1
                beta = min(beta, v)
                if v<=alpha :
                   return v
            return v


        #raise_not_defined()  # Remove this line once you finished your implementation
        # *** YOUR CODE GOES HERE ***

    def get_action(self, game_state):
        """ This method is called by the system to solicit an action from
            MinimaxAgent. It is passed in a State object.

            Like with all of the other search problems, we have abstracted
            away the details of the game state by producing a SearchProblem.
            You will use the states of this AdversarialSearchProblem to
            implement your minimax procedure. The details you need to know
            are explained at the top of this file.
        """
        # We tell the search problem what the current state is and which player
        # is the maximizing player (i.e. who's turn it is now).
        problem = AdversarialSearchProblem(game_state, self.max_player)
        state = problem.get_initial_state()
        utility, max_action = self.maximize(problem, state, 0)
        print("At Root: Utility:", utility, "Action:",
              max_action, "Expanded:", problem._expanded)
        return max_action

    def Result(self,problem,state,moves):
        # check=''
        # if moves=='East':
        #     check='West'
        for sub_state,action,cost in problem.get_successors(state):
            print('actions',action,'moves',moves)
            if action==moves:
                print('returning state',sub_state,'state',state)
                return state

