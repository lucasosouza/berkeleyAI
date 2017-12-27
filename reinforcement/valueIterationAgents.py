# valueIterationAgents.py
# -----------------------
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
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        state = mdp.getStartState()
        for i in range(0,iterations):
            #print "iteration: ", i
            #iterate once through all states and actions, save q-values
            for state in mdp.getStates():
                for action in mdp.getPossibleActions(state):
                    #compute qValue for each action
                    qValue = self.getQValue(state, action)
                    self.values[(state,action)] = qValue
            #after all qValues are computed, iterate againt through states, save value from optimal policy. these values will be V* for next iteration
            for state in mdp.getStates():
                action = self.getAction(state)
                self.values[state] = self.values[(state, action)] 

        """
        qValues = None
        if mdp.isTerminal(state):
            qValues = [v for k,v in self.values.items() if k == state]
        else:      
            qValues = [v for k,v in self.values.items() if k[0] == state]
        self.values[state] = max(qValues)

        for i in range(0, iterations):
            while not mdp.isTerminal(state):
                #selects the best action 
                action = self.computeActionFromValues(state)
                #stores the qValue
                self.values[state] = self.getQValue(state, action)
                #moves to the next state
                possibleStates = mdp.getTransitionStatesAndProbs(state, action)
                #chooses a path
                #print possibleStates
                state = util.chooseFromDistributionInverted(possibleStates)
                #if mdp.isTerminal(state): break

            # for state in mdp.getStates():
            #     if not mdp.isTerminal(state):
            #         for action in mdp.getPossibleActions():
            #             self.values[state] += self.getQValue(state, action)
        """

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qValue = 0
        statesProbs = self.mdp.getTransitionStatesAndProbs(state,action)
        #import pdb; pdb.set_trace()
        for nextState, prob in statesProbs:
            reward = self.mdp.getReward(state, action, nextState)
            #qValue += prob * (reward + self.discount * self.getValue(nextState))
            qValue += prob * (reward + self.discount * self.values[nextState])

        #I'm only saving q-values -> the value I get on the fly by looking for the best possible action and taking it
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None

        runningMax = -99999
        selectedAction = None
        for action in self.mdp.getPossibleActions(state):
            qValue = self.values[(state,action)]
            if qValue > runningMax:
                runningMax = qValue
                selectedAction = action

        return selectedAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
