from Networks.Network import Network
import random
import numpy as np

class Agent:
    def __init__(self, network):
        self.network = network
        self.fitness = 0

    def cross(self, otherAgent):
        childNetwork = Network.fromNetwork(self.network)
        for i in range(len(self.network.Layers)):
            thisLayer = self.network.Layers[i]
            otherLayer = otherAgent.network.Layers[i]
            childLayer = childNetwork.Layers[i]

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

    def mutate(self):
        for layer in self.network.Layers:
            #Choose a random row in each layer to mutate
            rowIndex = random.randint(0, len(layer.Weights) - 1) #Randint is inclusive
            mutationArray = np.random.normal(0,.01,len(layer.Weights[rowIndex]))
            layer.Weights[rowIndex] = np.add(layer.Weights[rowIndex],mutationArray)



