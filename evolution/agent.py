from networks.network import Network
from evolution.crossover import Crossover
from evolution.performance import Performance
import random
import numpy as np
from learningSettings import learningSettings

class Agent:
    def __init__(self, network):
        self.network = network
        self.performance = Performance()
        #Speciation variables
        self.maxEnergy = learningSettings.maxEnergy
        self.energy = learningSettings.initialEnergy

    def cross(self, otherAgent):
        childNetwork = Network.fromNetwork(self.network)
        for i in range(len(self.network.Layers)):
            thisLayer = self.network.Layers[i]
            otherLayer = otherAgent.network.Layers[i]
            childLayer = childNetwork.Layers[i]

            Crossover.crossUniform(thisLayer, otherLayer, childLayer)
        return Agent(childNetwork)

    def mutate(self):
        for layer in self.network.Layers:
            #Choose a random row in each layer to mutate
            rowIndex = random.randint(0, len(layer.Weights) - 1) #Randint is inclusive
            mutationArray = np.random.normal(0,.02,len(layer.Weights[rowIndex]))
            layer.Weights[rowIndex] = np.add(layer.Weights[rowIndex],mutationArray)

    def getPerformanceDistance(self, otherAgent):
        return self.performance.getJointHistoryDistance(otherAgent.performance)

    #Add an array of the current state of the agent
    def addToHistory(self, position, jointAngles):
        self.performance.addToHistory(position)
        self.performance.addToJointHistory(jointAngles)

    #Remove old history
    def resetHistory(self):
        self.performance = Performance()

    #Used for sorting populations
    def getFitness(self):
        return self.performance.getFitness()

    #Eat food if possible
    def eatFood(self, food):
        if(food.canBeEaten(self)):
            self.energy = min(self.energy + food.energy, self.maxEnergy)
            food.remainingUses = food.remainingUses - 1
            return True
        else:
            return False