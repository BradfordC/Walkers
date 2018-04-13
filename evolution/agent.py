from networks.network import Network
from evolution.crossover import Crossover
import random
import numpy as np
from learningSettings import learningSettings

class Agent:
    def __init__(self, network):
        self.network = network
        self.fitness = 0
        self.novelty = 0
        #Speciation variables
        self.maxEnergy = learningSettings.maxEnergy
        self.energy = learningSettings.initialEnergy
        #History of the agent during its generation, used for similarity testing
        self.history = []

    def cross(self, otherAgent):
        childNetwork = Network.fromNetwork(self.network)
        for i in range(len(self.network.Layers)):
            thisLayer = self.network.Layers[i]
            otherLayer = otherAgent.network.Layers[i]
            childLayer = childNetwork.Layers[i]

            Crossover.crossRandomType(thisLayer, otherLayer, childLayer)
        return Agent(childNetwork)

    def mutate(self):
        for layer in self.network.Layers:
            #Choose a random row in each layer to mutate
            rowIndex = random.randint(0, len(layer.Weights) - 1) #Randint is inclusive
            mutationArray = np.random.normal(0,.02,len(layer.Weights[rowIndex]))
            layer.Weights[rowIndex] = np.add(layer.Weights[rowIndex],mutationArray)

    #Add an array of the current state of the agent
    def addToHistory(self, stateArray):
        self.history.append(stateArray)

    #Remove old history
    def resetHistory(self):
        self.history = []

    #Compare the two agents' histories to see how different the two are
    def getHistoryDistance(self, otherAgentHistory):
        if(len(self.history) != len (otherAgentHistory)):
            print("Error: Histories are not the same size.")
            return None

        totalSquaredDifference = 0

        #For each state, check the difference between all values
        for stateIndex in range(len(self.history)):
            myState = self.history[stateIndex]
            otherState = otherAgentHistory[stateIndex]

            if(len(myState) != len(otherState)):
                print("Error: States are not the same size.")
                return None

            for i in range(len(myState)):
                totalSquaredDifference += (myState[i] - otherState[i]) ** 2

        distance = totalSquaredDifference ** 0.5
        return distance

    #Used for sorting populations
    def getFitness(self):
        return self.fitness

    #Eat food if possible
    def eatFood(self, food):
        if(food.canBeEaten(self)):
            self.energy = min(self.energy + food.energy, self.maxEnergy)
            food.remainingUses = food.remainingUses - 1
            return True
        else:
            return False