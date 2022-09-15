# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state
        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state
        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take
        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    current_state = problem.getStartState()
    to_search = util.Stack()
    to_search.push(current_state)
    # Remember each state's predecessor and direction for later
    directions = {}
    parent = ({current_state : None})   
    # Search the problem graph depth-first until the goal state is found.
    visited_states = set()  # Avoid duplicate computation by tracking visited states
    while not to_search.isEmpty():
        if current_state not in visited_states:
            if problem.isGoalState(current_state):
                break
            for successor in problem.getSuccessors(current_state):
                if successor[0] not in visited_states:
                    parent.update({successor[0] : current_state})
                    directions[successor[0]] = successor[1]
                    to_search.push(successor[0])
            visited_states.add(current_state)
        current_state = to_search.pop()

    # Build the list of moves by traversing backwards from the goal state to the start.
    return_directions = []
    while parent[current_state] is not None:
        return_directions.insert(0, directions[current_state])
        current_state = parent[current_state]

    return return_directions

def breadthFirstSearch(problem):
    current_state = problem.getStartState()
    to_search = util.Queue()
    to_search.push(current_state)
    # Remember each state's predecessor and direction for later
    directions = {}
    parent = ({current_state : None})   
    # Search the problem graph depth-first until the goal state is found.
    visited_states = set()  # Avoid duplicate computation by tracking visited states
    while not to_search.isEmpty():
        if current_state not in visited_states:
            if problem.isGoalState(current_state):
                break
            for successor in problem.getSuccessors(current_state):
                if successor[0] not in visited_states:
                    parent.update({successor[0] : current_state})
                    directions[successor[0]] = successor[1]
                    to_search.push(successor[0])
            visited_states.add(current_state)
        current_state = to_search.pop()

    # Build the list of moves by traversing backwards from the goal state to the start.
    return_directions = []
    while parent[current_state] is not None:
        return_directions.insert(0, directions[current_state])
        current_state = parent[current_state]

    return return_directions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch