from Networks import Network
from Evolution import Agent

class Population:
    def __init__(self, size, baseNetwork):
        self.AgentList = []

        layerSizes = baseNetwork.GetLayerSizes()

        for i in range(size):
            nextNetwork = Network.Network(layerSizes[0], layerSizes[-1], layerSizes[1:-1])
            nextAgent = Agent.Agent(nextNetwork)
            self.AgentList.append(nextAgent)

