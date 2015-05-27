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
from sets import Set
from util import Stack
from util import PriorityQueue

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
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    from game import Directions
    s = Directions.SOUTH; w = Directions.WEST; n = Directions.NORTH; s = Directions.SOUTH;

    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    unsolved = True
    state = problem.getStartState()
    visitedStates = Set([state]) # visited states as a set, helps to check if contains value x
    path = [] # path as a list
    startNode = [] #node as a list
    startNode.append(tuple([state]))
    fringe = PriorityQueue() # fringe as a priority queue
    fringe.push(startNode, 1)
    priorities = {'South': 1, 'West': 2, 'North': 3, 'East': 4} #priorities as dictionary
    #sucessor is an array with 3 items: path, direction, number of movements
    while True:
        currentNode = fringe.pop() #current Node is the last element on the fringe. element is then removed
        state = currentNode[-1][0] #state is the last state
        visitedStates.add(state) #add state to visited states, since is a graph traversal
        #if it finds, calculate the path based on the last node
        if problem.isGoalState(state):
            for node in currentNode[1:]:
                path.append(node[1])
            return path
        else: 
            #expansion. happens only once per node
            for successor in problem.getSuccessors(state):
                if successor[0] not in visitedStates:
                    successorNode = list(currentNode) #makes a deep copy of node
                    successorNode.append(successor) #adds the successor
                    fringe.push(successorNode,priorities[successor[1]])

    #end while loop        


    """ Test print statements
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    """

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

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
