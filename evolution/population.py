from networks import network
from evolution import agent, selection

import random

class Population:
    def __init__(self, size, baseNetwork):
        self.agentList = []

        layerSizes = baseNetwork.GetLayerSizes()

        for i in range(size):
            nextNetwork = network.Network(layerSizes[0], layerSizes[-1], layerSizes[1:-1])
            nextAgent = agent.Agent(nextNetwork)
            self.agentList.append(nextAgent)

    #Set the fitness of all agents
    def setFitness(self, walkerList):
        for i in range(len(walkerList)):
            walkerPosition = walkerList[i].getTorsoPosition()
            self.agentList[i].fitness = walkerPosition[0] + walkerPosition[1];

    #Cross agents to create another population
    def makeNextPopulation(self):
        nextPopulation = Population(len(self.agentList), self.agentList[0].network)
        for i in range(len(self.agentList)):
            #Pick a mate that isn't itself
            mate = i
            while(mate == i):
                mate = selection.TournamentSelect(self.agentList, 3)
            #Crossover with mate
            nextPopulation.agentList[i] = self.agentList[i].cross(self.agentList[mate])
        #Small chance of mutations
        nextPopulation.mutateAll(.1)

        return nextPopulation

    #Find the highest fitness value in the population
    def getHighestFitness(self):
        highestFitness = -999999999
        for agent in self.agentList:
            if(highestFitness < agent.fitness):
                highestFitness = agent.fitness
        return highestFitness

    #Try to mutate all agents with a certain chance of mutation
    def mutateAll(self, mutationChance):
        for agent in self.agentList:
            if(random.random() < mutationChance):
                agent.mutate()


