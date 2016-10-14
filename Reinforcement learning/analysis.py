# analysis.py
# -----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

def question2():
  answerDiscount = 0.9
  answerNoise = 0.01
  """Description:
  I lower the noise, so the agent becomes more brave and acrosses the bridge
  because it has lower chances to go to the undesire direction
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise

def question3a():
  answerDiscount = 0.3
  answerNoise = 0.01
  answerLivingReward = 0.0
  """Description:
  I lower the noise and discount to a certain point that the agent is brave enough
  to risk the cliff and finish the game early since the discount is low
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3b():
  answerDiscount = 0.03
  answerNoise = 0.02
  answerLivingReward = 0.1
  """Description:
  I did the same thing as 3a with some living reward. Thus the agent wants to be more safe
  while finishing the game early
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3c():
  answerDiscount = 0.9
  answerNoise = 0.05
  answerLivingReward = 0.0
  """Description:
  I lower the noise to a certain point that the agent is brave enough to risk the cliff.
  Since the discount is high, the agent wants to end with a higher reward exit.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3d():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 0.0
  """Description:
  I didn't change anything because the agent is safe enough to avoid the cliff while going to the 
  highest reward exit because it has high discount.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3e():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 1
  """Description:
  I changed the living reward to 1 so the agent wants to be safe and stay in the grid game forever.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question6():
  answerEpsilon = 0
  answerLearningRate = 1
  """Description:
  There is no possible answer because there's no optimal policy for this grid
  because the best solution is going to the east. However, since we still have 0.2 noise,
  the expect value for going east is still negative, so there's no optimal policy.
  """
  """ YOUR CODE HERE """
  return 'NOT POSSIBLE'
  """ END CODE """
  return answerEpsilon, answerLearningRate
  # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import analysis
  for q in [q for q in dir(analysis) if q.startswith('question')]:
    response = getattr(analysis, q)()
    print '  Question %s:\t%s' % (q, str(response))
