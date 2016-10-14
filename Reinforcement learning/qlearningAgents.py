# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discountRate (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)
    self.qvalue = util.Counter() #initialize the qvalue array



  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    """Description:
    Return the qValue for that (state,action)
    """
    """ YOUR CODE HERE """
    return self.qvalue[(state,action)]
    """ END CODE """



  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    """Description:
    Return 0 if there's no legal action
    Else, get the value by computing the maximum qValue.
    """
    """ YOUR CODE HERE """
    actions = self.getLegalActions(state) #get all the legal actions
    if not actions: #if there's no legal action, return 0
      return 0.0
    return max([self.getQValue(state,action) for action in actions]) #return the maximum qValue
    """ END CODE """

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    """Description:
    Obtain the policy with the maximum argument of the qValue and return it.
    """
    """ YOUR CODE HERE """
    actions = self.getLegalActions(state) #get all the legal actions
    if not actions: #if there's no legal action, return None
      return None
    value = float('-inf')  
    for action in actions: #for all the legal action
      q_value = self.getQValue(state,action) #get qValue
      if value <= q_value: #if the action has the maximum qValue, store that action as the policy
        value = q_value
        policy = action
    return policy  
    """ END CODE """

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    legalActions = self.getLegalActions(state)
    action = None

    """Description:
    Flip the coin base on the epsilon probability. If it's true, return a random action,
    else return the policy.
    """
    """ YOUR CODE HERE """
    if not legalActions: #if there's no action, return None
      return None
    if util.flipCoin(self.epsilon): #filp coin to determine we want the random action or policy
      action = random.choice(legalActions)
    else:
      action = self.getPolicy(state)
    """ END CODE """
    return action

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    """Description:
    Update the qValue using the q-learning equation from M4 slide 58
    """
    """ YOUR CODE HERE """
    sample = reward + self.discountRate * self.getValue(nextState) #sample of q-learning
    self.qvalue[(state,action)] = (1-self.alpha) * self.getQValue(state,action) + self.alpha * sample #sample based q-learning iteration

class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)

    # You might want to initialize weights here.
    self.weight = util.Counter() #initialze the weight array
    self.new_weight = util.Counter() #initialze the new weight array

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    """Description:
    Apply the approximate q-function from q9
    """
    """ YOUR CODE HERE """
    features = self.featExtractor.getFeatures(state, action) #get f(s,a) from the features
    return sum([features[feature] * self.weight[feature] for feature in features]) #apply the approximate q-function to get qValue
    """ END CODE """

  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    """Description:
    Apply the weight vector update equation from q9 to update the new weight array,
    the store the new weight array to the weight array
    """
    """ YOUR CODE HERE """
    features = self.featExtractor.getFeatures(state, action) #get f(s,a) from the features
    for feature in features: #for each feature
      correction = (reward + self.discountRate * self.getValue(nextState)) - self.getQValue(state, action) #compute the correction
      self.new_weight[feature] = self.weight[feature] + self.alpha * correction * features[feature] #compute the new weight
    self.weight = self.new_weight #store the new_weight when we finished update

  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      util.raiseNotDefined()
