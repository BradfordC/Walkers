from Networks.Network import Network
import random
import numpy as np

class Agent:
    def __init__(self, network):
        self.network = network
        self.fitness = 0

    def cross(self, otherAgent):
        childNetwork = Network(self.network.layerSizes[0], self.network.layerSizes[-1], self.network.layerSizes[1:-1])
        for i in range(len(self.network.Layers)):
            thisLayer = self.network.Layers[i]
            otherLayer = otherAgent.network.Layers[i]
            childLayer = childNetwork.Layers[i]

    def mutate(self):
        for layer in self.network.Layers:
            #Choose a random row in each layer to mutate
            rowIndex = random.randint(0, len(layer.Weights) - 1) #Randint is inclusive
            mutationArray = np.random.normal(0,.01,len(layer.Weights[rowIndex]))
            layer.Weights[rowIndex] = np.add(layer.Weights[rowIndex],mutationArray)



