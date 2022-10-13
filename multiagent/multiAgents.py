# multiAgents.py
# --------------
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


#from math import nextafter
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        ghostPositions = currentGameState.getGhostPositions()
        
        optimalScore = 0
        # Want to elimate needless pacman bot actions
        if action == "Stop":
            optimalScore = optimalScore - 50

        # Gets closest food with respect to how close a ghost is
        foodList = newFood.asList()
        foodDistances = [manhattanDistance(foodPos, newPos) for foodPos in foodList]
        if len(foodDistances) == 0:
            return 0
        shortestFood = min(foodDistances)
        ghostDistance = manhattanDistance(ghostPositions[0], newPos)

        return successorGameState.getScore() + (ghostDistance * 3) /  (shortestFood * 20) + optimalScore

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        action = self.max_value(gameState, 0, 0, "")
        return action[1]

    def value(self, gameState, index, depth, action):
        #if state is a terminal state (win/lose or depth reached)
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), action)
        if depth == self.depth:
            return (self.evaluationFunction(gameState), action)

        #if gamestate is 'pacman'
        if index == 0:
            return self.max_value(gameState, index, depth, action)
        #else gamestate is 'ghost'
        else:
            return self.min_value(gameState, index, depth, action)

    def max_value(self, gameState, index, depth, action):
        max = float("-inf")
        return_action = ""
        legalMoves = gameState.getLegalActions(index)
        for action in legalMoves:
            successor = gameState.generateSuccessor(index, action)

            #successor index moves back to pacman index
            if index + 1 == gameState.getNumAgents():
                successor_value = self.value(successor, 0, depth + 1, action)[0]
            else:
                successor_value = self.value(successor, index + 1, depth, action)[0]

            #maximize successor value over -inf
            if successor_value > max:
                max = successor_value
                return_action = action

        return (max, return_action)

    def min_value(self, gameState, index, depth, action):
        min = float("inf")
        return_action = ""
        legalMoves = gameState.getLegalActions(index)
        for action in legalMoves:
            successor = gameState.generateSuccessor(index, action)

          #successor index moves back to pacman index
            if index + 1 == gameState.getNumAgents():
                successor_value = self.value(successor, 0, depth + 1, action)[0]
            else:
                successor_value = self.value(successor, index + 1, depth, action)[0]

            #minimize successor value over inf
            if successor_value < min:
                min = successor_value
                return_action = action

        return (min, return_action)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        action = self.max_value_pruning(gameState, 0, 0, float("-inf"), float("inf"))
        return action[1]

    def value(self, gameState, index, depth, action, alpha, beta):
        #if state is a terminal state (win/lose or depth reached)
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), action, alpha, beta)
        if depth == self.depth:
            return (self.evaluationFunction(gameState), action, alpha, beta)

        #if gamestate is 'pacman'
        if index == 0:
            return self.max_value_pruning(gameState, index, depth, alpha, beta)
        #else gamestate is 'ghost'
        else:
            return self.min_value_pruning(gameState, index, depth, alpha, beta)

    def max_value_pruning(self, gameState, index, depth, alpha, beta):
        max = float("-inf")
        return_action = ""
        legalMoves = gameState.getLegalActions(index)
        for action in legalMoves:
            successor = gameState.generateSuccessor(index, action)

          #successor index moves back to pacman index
            if index + 1 == gameState.getNumAgents():
                successor_value = self.value(successor, 0, depth + 1, action, alpha, beta)[0]
            else:
                successor_value = self.value(successor, index + 1, depth, action, alpha, beta)[0]
            #minimize successor value over inf
            if successor_value > max:
                max = successor_value
                return_action = action

            #alpha-beta pruning implementation
            if max > beta:
                return (max, action, alpha, beta)
            #minimize successor value over inf
            if alpha < max:
                alpha = max

        return (max, return_action, alpha, beta)

    def min_value_pruning(self, gameState, index, depth, alpha, beta):
        min = float("inf")
        return_action = ""
        legalMoves = gameState.getLegalActions(index)
        for action in legalMoves:
            successor = gameState.generateSuccessor(index, action)

          #successor index moves back to pacman index
            if index + 1 == gameState.getNumAgents():
                successor_value = self.value(successor, 0, depth + 1, action, alpha, beta)[0]
            else:
                successor_value = self.value(successor, index + 1, depth, action, alpha, beta)[0]
            #minimize successor value over inf
            if successor_value < min:
                min = successor_value
                return_action = action

            #alpha-beta pruning implementation
            if min < alpha:
                return (min, action, alpha, beta)
            #minimize successor value over inf
            if beta > min:
                beta = min

        return (min, return_action, alpha, beta)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
