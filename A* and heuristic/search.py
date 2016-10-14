# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def startingState(self):
    """
    Returns the start state for the search problem 
    """
    util.raiseNotDefined()

  def isGoal(self, state): #isGoal -> isGoal
    """
    state: Search state

    Returns True if and only if the state is a valid goal state
    """
    util.raiseNotDefined()

  def successorStates(self, state): #successorStates -> successorsOf
    """
    state: Search state
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
    """
    util.raiseNotDefined()

  def actionsCost(self, actions): #actionsCost -> actionsCost
    """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
    """
    util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.startingState()
  print "Is the start a goal?", problem.isGoal(problem.startingState())
  print "Start's successors:", problem.successors(problem.startingState())
  """
  '''
  In dfs, I followed the graph search algorithm and let the fringe be the stack.
  '''
  start = (problem.startingState(),[]) #initial state, list for keep track of the actions
  S = util.Stack() #use the stack as the fringe to keep track all the reachable states
  S.push(start) # push the starting state
  visited=set() # create an empty set to keep track of the visited state
  while(True):
    if(S.isEmpty()): #if stack is empty and we didn't reach the goal state, then there's no solution for this problem
      return False
    state,action = S.pop() #pop out the current state
    if(problem.isGoal(state)):
      return action #return the action to reach the goal state
    if state not in visited: #do the following for all the unvisited state
      visited.add(state) #mark the current state as visited
      for i in problem.successorStates(state): 
        S.push((i[0],action+[i[1]])) #push the (state, actions) for each successor state


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  '''
  In bfs, I did the same thing as dfs but just changed the fringe into queue.
  '''
  start = (problem.startingState(),[]) #initial state, list for keep track of the actions
  S = util.Queue() #for bfs, we use queue as the fringe to keep track all the reachable states
  S.push(start) # push the starting state
  visited=set() # create an empty set to keep track of the visited state
  while(True):
    if(S.isEmpty()): #if queue is empty and we didn't reach the goal state, then there's no solution for this problem
      return False
    state,action = S.pop() #pop out the current state
    if(problem.isGoal(state)):
      return action #return the action to reach the goal state
    if state not in visited: #do the following for all the unvisited state
      visited.add(state) #mark the current state as visited
      for i in problem.successorStates(state):
        S.push((i[0],action+[i[1]]))  #push the (state, actions) for each successor state

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  '''
  In ucs, I changed the fringe to priority queue and let the cost be the priority.
  '''
  start = (problem.startingState(), [],0) #initial state, list for keep track of the actions and costs
  S = util.PriorityQueue() #for ucs, we use PriorityQueue as fringe
  S.push(start,0)  # push the starting state
  visited=set() # create an empty set to keep track of the visited state
  while(True):
    if(S.isEmpty()): #if priority queue is empty and we didn't reach the goal state, then there's no solution for this problem
      return False
    state,action,cost = S.pop() #pop out the current state
    if(problem.isGoal(state)):
      return action #return the action to reach the goal state
    if state not in visited: #do the following for all the unvisited state
      visited.add(state) #mark the current state as visited
      for i in problem.successorStates(state):
        S.push((i[0],action+[i[1]],cost + i[2]),cost + i[2]) 
        #push the (state, actions, total cost) for each successor state with the total cost as the priority

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  '''
  In aStarSearch, I changed the fringe to PriorityQueueWithFunction and 
  set the priority be total cost + heuristic.
  '''
  start = (problem.startingState(), [],0) #initial state, list for keep track of the actions and costs
  priority = lambda node: node[2] + heuristic(node[0],problem) #set the priority base on g(n) + h(n)
  S = util.PriorityQueueWithFunction(priority) #for a* search, we use PriorityQueueWithFunction as fringe
  S.push(start) # push the starting state
  visited=set() # create an empty set to keep track of the visited state
  while(True):
    if(S.isEmpty()): 
    #if PriorityQueueWithFunction is empty and we didn't reach the goal state, then there's no solution for this problem
      return False
    state,action,cost = S.pop() #pop out the current state
    if(problem.isGoal(state)):
      return action #return the action to reach the goal state
    if state not in visited: #do the following for all the unvisited state
      visited.add(state) #mark the current state as visited
      for i in problem.successorStates(state):
        S.push((i[0],action+[i[1]],cost + i[2]))
        #push the (state, actions, total cost) for each successor state with the total cost + heuristic as the priority


  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
