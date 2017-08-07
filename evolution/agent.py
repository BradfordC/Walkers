from networks.network import Network
import random
import numpy as np
from learningSettings import learningSettings

class Agent:
    def __init__(self, network):
        self.network = network
        self.fitness = 0
        self.novelty = 0
        #Speciation variables
        self.maxEnergy = learningSettings.initialEnergy
        self.energy = self.maxEnergy
        #History of the agent during its generation, used for similarity testing
        self.history = []

    def cross(self, otherAgent):
        childNetwork = Network.fromNetwork(self.network)
        for i in range(len(self.network.Layers)):
            thisLayer = self.network.Layers[i]
            otherLayer = otherAgent.network.Layers[i]
            childLayer = childNetwork.Layers[i]

            #For each row of weights, pick a random point
            #The weights before that point come from this parent, the ones after come from the other
            for row in range(len(thisLayer.Weights)):
                thisLayerRow = thisLayer.Weights[row]
                otherLayerRow = otherLayer.Weights[row]
                childLayerRow = childLayer.Weights[row]

                crossoverPoint = random.randint(1,len(thisLayer.Weights[row]) - 1)
                for column in range(len(thisLayer.Weights[row])):
                    if(column < crossoverPoint):
                        childLayerRow[column] = thisLayerRow[column]
                    else:
                        childLayerRow[column] = otherLayerRow[column]
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

    #Compare the two agents' histories to see how different the two are
    def getDifference(self, otherAgent):
        if(len(self.history) != len (otherAgent.history)):
            print("Error: Histories are not the same size.")
            return None

        totalDifference = 0

        #For each state, check the difference between all values
        for stateIndex in range(len(self.history)):
            myState = self.history[stateIndex]
            otherState = otherAgent.history[stateIndex]

            if(len(myState) != len(otherState)):
                print("Error: States are not the same size.")
                return None

            for i in range(len(myState)):
                totalDifference += abs(myState[i] - otherState[i])

        return totalDifference