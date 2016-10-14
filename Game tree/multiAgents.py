# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    some Directions.X for some X in the set {North, South, West, East, Stop}
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
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPosition = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    '''
    This evaluation is based on the distance of the closest food 
    and the distance of the ghosts with newScaredTimes.
    '''
    evaluation = 0 #initialize the evaluation to 0
    if newPosition in oldFood.asList(): #if there's food at the next action, add 10 points
      evaluation+=10
    else: #if there's no food at the next action, give points according to the distance of the closest food
      evaluation+= (8.0/min([util.manhattanDistance(newPosition,i)for i in oldFood.asList()])) 
    #calculate the coordinate for next action's surrounding    
    surrounding = [(newPosition[0]-1,newPosition[1]),(newPosition[0],newPosition[1]-1),(newPosition[0]+1,newPosition[1]),(newPosition[0],newPosition[1]+1)]
    for i in surrounding: #if the action's surroundings have ghosts, minus 12 points
      for j in newGhostStates:
        if (j.getPosition() == i) | (j.getPosition() == newPosition):
          evaluation-=12
    for i in newGhostStates: 
      ghostDistance = util.manhattanDistance(newPosition,i.getPosition()) #get the distance between pacman and the ghosts
      if ghostDistance == 0: #because 0 can't be divisible, change it to a very small number
        ghostDistance = 0.000000001
      #if newScaredTimes is greater than 0 and pacman can chase the ghosts within time,
      #add points to evaluation. Else if pacman is too close to the ghosts, subtract points to 
      #make pacman to go away
      if newScaredTimes[0] > 0 and ghostDistance <= newScaredTimes[0]/1.5: 
        evaluation+=(newScaredTimes[0]*(1.0/ghostDistance)*10)
      elif ghostDistance <=3:
        evaluation-=8     
    return evaluation

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
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.treeDepth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.treeDepth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    move, result = self.value(gameState, 0)
    return move

  def value(self, state, maxMin): 
    if maxMin == self.treeDepth * state.getNumAgents(): #if we reach the leaves of the tree, return the terminal value
      return [Directions.STOP,self.evaluationFunction(state)]
    elif maxMin % state.getNumAgents() == 0: #if the current depth has remainder of 0, that means is pacman's turn
      return self.max_value(state,maxMin)
    else: #else is ghost's turn
      return self.min_value(state,maxMin)

  def max_value(self,state,maxMin):
    Max = [Directions.STOP,float('-inf')] #set the max value to negative infinite
    successor = state.getLegalActions(maxMin%state.getNumAgents()) #get all the legal action of the current state
    if not successor: #if there's no legal action, this is a terminal state
      return [Directions.STOP,self.evaluationFunction(state)]
    for i in successor: #for each action, we get the value of its successor and return the maximum one
      success = state.generateSuccessor(maxMin % state.getNumAgents(),i)
      success,value = self.value(success,maxMin+1)
      if value > Max[1]:
        Max = [i,value]
    return Max

  def min_value(self,state,maxMin):
    Min = [Directions.STOP,float('inf')] #set the min value to infinite
    successor = state.getLegalActions(maxMin%state.getNumAgents()) #get all the legal action of the current state
    if not successor: #if there's no legal action, this is a terminal state
      return [Directions.STOP,self.evaluationFunction(state)]
    for i in successor: #for each action, we get the value of its successor and return the minimum one
      success = state.generateSuccessor(maxMin % state.getNumAgents(),i)
      success,value = self.value(success,maxMin+1)
      if value < Min[1]:
        Min = [i, value]
    return Min

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.treeDepth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    move, result = self.alpha_beta_search(gameState, 0)
    return move

  def alpha_beta_search(self, state, maxMin):
    v = self.max_value(state,maxMin,float('-inf'),float('inf')) #call the initial max_value with negative inf for alpha and inf for beta
    return v

  def max_value(self,state,maxMin,alpha,beta):
    Max = [Directions.STOP,float('-inf')] #set the max value to negative infinite
    successor = state.getLegalActions(maxMin%state.getNumAgents())
    if maxMin == self.treeDepth * state.getNumAgents() or not successor: #if there's no legal action or it's the leaves, then is a terminal state
      return [Directions.STOP,self.evaluationFunction(state)]
    for i in successor: #for each action, we get the value of its successor and return the maximum one
      success = state.generateSuccessor(maxMin % state.getNumAgents(),i)
      success,value = self.min_value(success,maxMin+1,alpha,beta)
      if value > Max[1]:
        Max = [i,value]
      if Max[1] >= beta: #if the max value is greater than beta, return max
        return Max
      alpha = max(alpha,Max[1]) #update alpha value
    return Max

  def min_value(self,state,maxMin,alpha,beta):
    Min = [Directions.STOP,float('inf')] #set the min value to infinite
    successor = state.getLegalActions(maxMin%state.getNumAgents())
    if maxMin == self.treeDepth * state.getNumAgents() or not successor: #if there's no legal action or it's the leaves, then is a terminal state
      return [Directions.STOP,self.evaluationFunction(state)]
    for i in successor: #for each action, we get the value of its successor and return the minimum one
      success = state.generateSuccessor(maxMin%state.getNumAgents(),i)
      if (maxMin+1)%state.getNumAgents() ==0: #if the next turn is pacman's turn, call max_value
        success,value = self.max_value(success,maxMin+1,alpha,beta)
      else: #else is ghost's turn, call min_value
        success,value = self.min_value(success,maxMin+1,alpha,beta)  
      if value < Min[1]:
        Min = [i, value]
      if Min[1] <= alpha: #if the min value is greater than alpha, return min
        return Min
      beta = min(beta,Min) #update beta value    
    return Min

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.treeDepth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    move, result = self.value(gameState, 0)
    return move

  def value(self, state, maxMin):
    if maxMin == self.treeDepth * state.getNumAgents(): #if we reach the leaves of the tree, return the terminal value
      return [Directions.STOP,self.evaluationFunction(state)]
    if maxMin%state.getNumAgents() ==0:  #if the current depth has remainder of 0, that means is pacman's turn
      return self.max_value(state,maxMin)
    else: #else is ghost's turn
      return self.exp_value(state,maxMin)

  def max_value(self,state,maxMin):
    Max = [Directions.STOP,float('-inf')] #set the max value to negative infinite
    successor = state.getLegalActions(maxMin%state.getNumAgents())  #get all the legal action of the current state
    if not successor: #if there's no legal action, this is a terminal state
      return [Directions.STOP,self.evaluationFunction(state)]
    for i in successor:  #for each action, we get the value of its successor and return the maximum one
      success = state.generateSuccessor(maxMin % state.getNumAgents(),i)
      success,value = self.value(success,maxMin+1)
      if value > Max[1]:
        Max = [i,value]
    return Max

  def exp_value(self,state,maxMin):
    successor = state.getLegalActions(maxMin%state.getNumAgents()) #get all the legal action of the current state
    if not successor: #if there's no legal action, this is a terminal state
      return [Directions.STOP,self.evaluationFunction(state)]    
    prob = 1.0/len(successor) #The probability is 1/the number of successor state
    expectimax = 0 #initialize expectimax to 0
    for i in successor:  #for each action, we get the value of its successor and calculate the expectimax
      success = state.generateSuccessor(maxMin % state.getNumAgents(),i)
      success,value = self.value(success,maxMin+1)
      expectimax += value * prob #add value * probability to expectimax since E(x) = sum(p(x)x)
    return [Directions.STOP,expectimax]

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  '''
  This evaluation is based on the distance of the closest food 
  and the distance of each ghost with newScaredTimes.
  '''
  newPosition = currentGameState.getPacmanPosition()
  oldFood = currentGameState.getFood()
  newGhostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

  evaluation = currentGameState.getScore() #set the score of the current state as the initial evaluation, so we know whether is winning or losing
  if not oldFood.asList(): #if there's no more food, return a high evaluation to represent victory
    return 999
  if newPosition in oldFood.asList(): #if there's food at the next action, add 20 points
    evaluation+=20
  else:  #if there's no food at the next action, give points according to the distance of the closest food
    evaluation+= (15.0/min([util.manhattanDistance(newPosition,i)for i in oldFood.asList()]))   
  #calculate the coordinate for current state's surrounding  
  surrounding = [(newPosition[0]-1,newPosition[1]),(newPosition[0],newPosition[1]-1),(newPosition[0]+1,newPosition[1]),(newPosition[0],newPosition[1]+1)]
  for i in surrounding:
    if i in oldFood.asList(): #add points if the surroundings have foods
      evaluation+=2
    for j,items in enumerate(newGhostStates):
      if items.getPosition() == newPosition: #if pacman hits the ghost, return a low evalution to represent defeated
        return -999
      if (items.getPosition() == i): #if the state's surroundings have ghosts, minus 12 points
        evaluation-=12
  for i,items in enumerate(newGhostStates):
    ghostDistance = util.manhattanDistance(newPosition,items.getPosition())  #get the distance between pacman and the ghosts
    if ghostDistance == 0: #because 0 can't be divisible, change it to a very small number
      ghostDistance = 0.000000001 
    #if newScaredTimes is greater than 0 and pacman can chase the ghosts within time,
    #add points to evaluation. Else if pacman is too close to the ghosts, subtract points to 
    #make pacman to go away   
    if newScaredTimes[i] > 0 and ghostDistance <= newScaredTimes[i]/1.5:
      evaluation+=(newScaredTimes[i]*(1.0/ghostDistance)*15)
    elif ghostDistance <=4:
      evaluation-=10   
  return evaluation #return the total score for evalutation
# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

