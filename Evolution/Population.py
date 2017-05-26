from Networks import Network
from Evolution import Agent

class Population:
    def __init__(self, size, baseNetwork):
        self.agentList = []

        layerSizes = baseNetwork.GetLayerSizes()

        for i in range(size):
            nextNetwork = Network.Network(layerSizes[0], layerSizes[-1], layerSizes[1:-1])
            nextAgent = Agent.Agent(nextNetwork)
            self.agentList.append(nextAgent)

    def makeNextPopulation(self):
        return self

    def getHighestFitness(self):
        highestFitness = -999999999
        for agent in self.agentList:
            if(highestFitness < agent.fitness):
                highestFitness = agent.fitness
        return highestFitness

