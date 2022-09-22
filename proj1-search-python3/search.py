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
    # Remember the path to each stated
    path_to = ({current_state: []})
    # Search the problem graph depth-first until the goal state is found.
    visited_states = set()  # Avoid duplicate computation by tracking visited states
    while not to_search.isEmpty():
        current_state = to_search.pop()
        if problem.isGoalState(current_state):
            return path_to[current_state]
        if current_state not in visited_states:
            visited_states.add(current_state)
            for successor in problem.getSuccessors(current_state):
                if successor[0] not in visited_states:
                    path_to.update({successor[0]: path_to[current_state] + [successor[1]]})
                    to_search.push(successor[0])
   

def breadthFirstSearch(problem):
    current_state = problem.getStartState()
    # print(current_state)
    to_search = util.Queue()
    to_search.push(current_state)
    parent = {current_state : (None, None)}
    # print("Start dict: " + str(path_to))
    # Search the problem graph depth-first until the goal state is found.
    visited_states = set()  # Avoid duplicate computation by tracking visited states
    while not to_search.isEmpty():
        current_state = to_search.pop()
        visited_states.add(current_state)
        # print(visited_states)
        if problem.isGoalState(current_state):
            break
        for successor in problem.getSuccessors(current_state):
            if successor[0] not in to_search.list and successor[0] not in visited_states:
                parent[successor[0]] = (current_state, successor[1])
                to_search.push(successor[0])
    path = []
    while parent[current_state][0]:
        path.insert(0, parent[current_state][1])
        current_state = parent[current_state][0]
    print(path)
    return path



def uniformCostSearch(problem):
    current_state = problem.getStartState()
    to_search = util.PriorityQueue()
    to_search.push(current_state, 0)

    to_search_list = []
    to_search_list.append(current_state)

    # Remember the path to each stated
    path_to = ({current_state: []})
    visited_states = set()
    visited_states_values = {}
    visited_states_values[current_state] = 0
    while not to_search.isEmpty():
        current_state = to_search.pop()
        to_search_list.remove(current_state)
        if problem.isGoalState(current_state):
            return path_to[current_state]
        if current_state not in visited_states:
            visited_states.add(current_state)
            for successor in problem.getSuccessors(current_state):
                successor_cost = visited_states_values[current_state] + successor[2]
                if successor[0] in to_search_list:
                    if visited_states_values[successor[0]] > successor_cost:
                        path_to.update({successor[0]: path_to[current_state] + [successor[1]]})
                        to_search.update(successor[0], successor_cost)
                        visited_states_values[successor[0]] = successor_cost
                elif successor[0] not in visited_states:
                    path_to.update({successor[0]: path_to[current_state] + [successor[1]]})
                    to_search.push(successor[0], successor_cost)
                    to_search_list.append(successor[0])
                    visited_states_values[successor[0]] = successor_cost

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    current_state = problem.getStartState()
    to_search = util.PriorityQueue()
    to_search.push(current_state, heuristic(current_state, problem))

    to_search_list = []
    to_search_list.append(current_state)

    # Remember the path to each stated
    path_to = ({current_state: []})
    visited_states = set()
    visited_states_values = {}
    visited_states_values[current_state] = heuristic(current_state, problem)
    while not to_search.isEmpty():
        current_state = to_search.pop()
        to_search_list.remove(current_state)
        if problem.isGoalState(current_state):
            return path_to[current_state]
        if current_state not in visited_states:
            visited_states.add(current_state)
            for successor in problem.getSuccessors(current_state):
                successor_cost = visited_states_values[current_state] + successor[2] + heuristic(successor[0], problem)
                if (successor[0] in to_search_list) and (visited_states_values[successor[0]] > successor_cost):
                        path_to.update({successor[0]: path_to[current_state] + [successor[1]]})
                        to_search.update(successor[0], successor_cost)
                        visited_states_values[successor[0]] = visited_states_values[current_state] + successor[2]
                elif successor[0] not in visited_states:
                    if successor[0] not in to_search_list:
                        path_to.update({successor[0]: path_to[current_state] + [successor[1]]})
                    to_search.push(successor[0], successor_cost)
                    to_search_list.append(successor[0])
                    visited_states_values[successor[0]] = visited_states_values[current_state] + successor[2]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch