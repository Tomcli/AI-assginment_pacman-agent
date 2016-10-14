# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discountRate = 0.9, iters = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discountRate = discountRate
    self.iters = iters
    self.values = util.Counter() # A Counter is a dict with default 0

    """Description:
    First I initiallize 2 arrays to represent V(k) and V(k-1)
    Then for each state, we cheak if it's terminal or not. 
    If the state is terminal, set the state value to 0.
    Else, apply the bellman's equation to obtain the values and store to
    V(k). Do the above step for k iterations to finalize V(k) for getValue
    and getPolicy.
    """
    """ YOUR CODE HERE """
    self.current = self.mdp.getStates() #get the list of states
    self.values = util.Counter() #initialize the value array.
    self.new = self.values #initialize the new value array. 
    for i in range(self.iters): #do the following for k iterations
      self.new = util.Counter() #reinitialze the new array so it won't update the state value that's not in self.current
      for state in self.current: #for each state
        if self.mdp.isTerminal(state): #if the state is in terminal, set the value to 0 and continue with a new loop
          self.new[state] = 0
          continue
        actions = self.mdp.getPossibleActions(state) #get all the possible actions
        value = max([self.getQValue(state,action) for action in actions]) #The value is the maximum of all the qValue
        self.new[state] = value #store the value to the array
      self.values = self.new #update the new values
    """ END CODE """

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """

    """Description:
    The value of the state was computed in in __init__, 
    so I just return the value for that state.
    """
    """ YOUR CODE HERE """
    return self.values[state]
    """ END CODE """

  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    """Description:
    I apply the bellman's equation here to computed the qValue
    """
    """ YOUR CODE HERE """
    transition = self.mdp.getTransitionStatesAndProbs(state,action) #get all the possible transition
    reward = 0
    previous_value = 0
    q_value =0
    for nextState in transition: 
      reward = self.mdp.getReward(state, action, nextState[0]) #computed the reward of the bellman's equation
      q_value += nextState[1]*(reward + self.discountRate*self.values[nextState[0]]) #computed the bellman's equation
    return q_value

    """ END CODE """

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """

    """Description:
    I apply the bellman's equation to obtain pi star which is the maximum
    argument of the qValue.
    """
    """ YOUR CODE HERE """
    if self.mdp.isTerminal(state): #if the state is terminal, return None
      return None
    actions = self.mdp.getPossibleActions(state) #get all the possible action
    value = float('-inf')
    policy = None
    for action in actions:  #for each action
      q_value = self.getQValue(state,action) #get the qValue for that action
      if value <= q_value: #if the qValue is the maximum set policy to that action
        value = q_value
        policy = action
    return policy
    """ END CODE """

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
