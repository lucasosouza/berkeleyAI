# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        #self.values = util.Counter()
        self.qValues = util.Counter()
        self.stateProbs = dict()
        self.rewards = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"

        return self.qValues[(state,action)]

        """
        qValue = 0
        statesProbs = self.getTransitionStatesAndProbs(state,action)
        if len(statesProbs) == 0: return 0.0
        for nextState, prob in statesProbs:
            reward = self.rewards[(state, action, nextState)]
            nextStateQValues = [v for k,v in self.qValues if k[0] == nextState]
            vStar = 0
            if len(nextStateQValues) > 0:
                vStar = max(nextStateQValues)
            qValue += prob * (reward + self.discount * vStar)
        return qValue    
        """

    """ not really necessary -- I was too attached to MDP way of solving the problem
    in q-learning there is no need to store the probability to each stateProbs
    you learn by simply observing action and reward

    def getTransitionStatesAndProbs(self, state, action):
        transitions = []
        #print "evaluating state: ", state
        if (state,action) in self.stateProbs:
            total = self.stateProbs[(state,action)].totalCount()
            for nextState, count in self.stateProbs[(state,action)].items():
                #print "total is: ", state, count, total, (nextState, float(count/total))
                transitions.append((nextState, float(count/total)))
        return transitions

    """

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        possibleActions = self.getLegalActions(state)
        if len(possibleActions) == 0: return 0.0

        qValues = [self.getQValue(state,action) for action in possibleActions]
        return max(qValues)

        return futureValue

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        #maxValue = self.getValue(state)
        possibleActions = self.getLegalActions(state)
        if len(possibleActions) == 0:
            return None

        actions = util.Counter()
        for action in self.getLegalActions(state):
            actions[action] = self.getQValue(state,action)

        #get max values and randomly select between ties
        maxValue = max(actions.values())
        selectedActions = [k for k,v in actions.items() if v == maxValue]
        if len(selectedActions) > 1:
            selectedAction = random.choice(selectedActions)
        else:
            selectedAction = selectedActions[0]

        return selectedAction

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
        possibleActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        if len(possibleActions) == 0: return None
        if util.flipCoin(self.epsilon):
            action = random.choice(possibleActions)
        else:
            action = self.getPolicy(state)

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #learn the probability
        if not (state,action) in self.stateProbs:
            self.stateProbs[(state,action)] = util.Counter()
        self.stateProbs[(state,action)][nextState] += 1.0
        self.qValues[(state, action)] = (1-self.alpha)*self.getQValue(state,action)+(self.alpha)*(reward+self.discount*self.getValue(nextState))

        """
        attempts

        #1-alpha the expected q value + alpha(reward got + nextState q value)


        #print "Q-values: ", self.qValues

        #update the value
        #self.values[state] += self.alpha*(self.getValue(state) - self.values[state])
        #print "values: ", self.values

        #debugging

        #print "stateProbs: ", self.stateProbs

        #learn the reward
        #self.rewards[(state, action, nextState)] += self.alpha*(reward - self.rewards[(state, action, nextState)]) 


        #self.rewards[(state, action, nextState)] = reward
        #print "rewards: ", self.rewards

        #update the q-value

        """

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


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
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        weights = self.getWeights()
        feats = self.featExtractor.getFeatures(state,action)
        qValue = reduce(lambda x,y: x+y, [weights[f]*v for f,v in feats.items()])
        return qValue

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
       #update weights
        weights = self.getWeights()
        difference = (reward + self.discount*self.getValue(nextState)) - self.getQValue(state, action)
        for f in self.featExtractor.getFeatures(state,action).keys():
            weights[f] += self.alpha*difference

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
