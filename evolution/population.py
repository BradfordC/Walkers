from networks import network
from evolution import agent, selection
from learningSettings import learningSettings

import random

class Population:
    def __init__(self, size=0, baseNetwork=None):
        self.agentList = []

        if(size > 0):
            layerSizes = baseNetwork.GetLayerSizes()

            for i in range(size):
                nextNetwork = network.Network(layerSizes[0], layerSizes[-1], layerSizes[1:-1])
                nextAgent = agent.Agent(nextNetwork)
                self.agentList.append(nextAgent)

    #Set the fitness of all agents
    def setFitness(self, walkerList):
        for i in range(len(self.agentList)):
            walkerPosition = walkerList[i].getTorsoPosition()
            self.agentList[i].fitness = walkerPosition[0]# + walkerPosition[1]

    #Find out how novel each agent is
    def setNovelty(self):
        #Make sure all novelties are set to 0, since we'll be adding to them
        for agent in self.agentList:
            agent.novelty = 0

        #Novelty is based on the difference between an agent and all other agents
        for i in range(len(self.agentList)):
            for j in range(i + 1, len(self.agentList)):
                firstAgent = self.agentList[i]
                secondAgent = self.agentList[j]
                difference = firstAgent.getHistoryDistance(secondAgent.history)
                firstAgent.novelty += difference
                secondAgent.novelty += difference

        #Get the average novelty
        for agent in self.agentList:
            agent.novelty /= len(self.agentList)

    #Calculate the fitness for each agent
    def calculateFitness(self, walkerList, selectionCriteria):
        if(selectionCriteria == selection.OBJECTIVE
                   or selectionCriteria == selection.SPECIATION):
            self.setFitness(walkerList)
            print(str(self.getAverageFitness()) + "\t" + str(self.getHighestFitness()))
        elif(selectionCriteria == selection.NOVELTY):
            self.setNovelty()
            print(self.getHighestNovelty())
        elif(selectionCriteria == selection.COMBINED):
            self.setFitness(walkerList)
            self.setNovelty()
            print(str(self.getAverageFitness()) + "\t" + str(self.getHighestFitness()))

    #Sort the population so it starts with the agent with the highest fitness
    def sortByFitness(self):
        self.agentList.sort(key=agent.Agent.getFitness, reverse=True)


    #Cross agents to create another population
    def makeNextPopulation(self, walkerList, selectionCriteria):
        nextPopulation = Population(len(self.agentList), self.agentList[0].network)
        for i in range(len(self.agentList)):
            #Pick a mate that isn't itself
            mate = i
            while(mate == i):
                mate = selection.TournamentSelect(self.agentList, learningSettings.tournamentSize, selectionCriteria)
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

    def getAverageFitness(self):
        fitnessSum = 0
        for agent in self.agentList:
            fitnessSum += agent.fitness
        return fitnessSum / len(self.agentList)

    # Find the highest novelty value in the population
    def getHighestNovelty(self):
        highestNovelty = -999999999
        for agent in self.agentList:
            if (highestNovelty < agent.novelty):
                highestNovelty = agent.novelty
        return highestNovelty

    def getAverageNovelty(self):
        noveltySum = 0
        for agent in self.agentList:
            noveltySum += agent.novelty
        return noveltySum / len(self.agentList)

    #Try to mutate all agents with a certain chance of mutation
    def mutateAll(self, mutationChance):
        for agent in self.agentList:
            if(random.random() < mutationChance):
                agent.mutate()


