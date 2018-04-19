from networks import network
from evolution import agent, selection
from learningSettings import learningSettings
import pickle
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

    #Return the size of the population
    def size(self):
        return len(self.agentList)

    #Calculate the novelty for each agent in the population
    def setNovelty(self):
        performanceList = [agent.performance for agent in self.agentList]
        for performance in performanceList:
            performance.setNovelty(performanceList)

    #Print the score for each agent
    def printScore(self, selectionCriteria):
        if(selectionCriteria == selection.OBJECTIVE or selectionCriteria == selection.SPECIATION):
            print(str(self.getAverageFitness()) + "\t" + str(self.getHighestFitness()))
        elif(selectionCriteria == selection.NOVELTY):
            print(self.getHighestNovelty())
        elif(selectionCriteria == selection.COMBINED):
            print(str(self.getAverageFitness()) + "\t" + str(self.getHighestFitness()))

    #Sort the population so it starts with the agent with the highest fitness
    def sortByFitness(self):
        self.agentList.sort(key=agent.Agent.getFitness, reverse=True)

    #Cross agents to create another population
    def makeNextPopulation(self, selectionCriteria):
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
            if(highestFitness < agent.performance.getFitness()):
                highestFitness = agent.performance.getFitness()
        return highestFitness

    def getAverageFitness(self):
        fitnessSum = 0
        for agent in self.agentList:
            fitnessSum += agent.performance.getFitness()
        return fitnessSum / len(self.agentList)

    # Find the highest novelty value in the population
    def getHighestNovelty(self):
        highestNovelty = -999999999
        for agent in self.agentList:
            if (highestNovelty < agent.performance.getNovelty()):
                highestNovelty = agent.performance.getNovelty()
        return highestNovelty

    def getAverageNovelty(self):
        noveltySum = 0
        for agent in self.agentList:
            noveltySum += agent.performance.getNovelty()
        return noveltySum / len(self.agentList)

    #Try to mutate all agents with a certain chance of mutation
    def mutateAll(self, mutationChance):
        for agent in self.agentList:
            if(random.random() < mutationChance):
                agent.mutate()

    #Save the current population to a file
    def saveToFile(self, fileName):
        with open(fileName, 'wb') as file:
            pickle.dump(self.agentList, file, pickle.HIGHEST_PROTOCOL)

    #Load agents from a file
    @classmethod
    def loadFromFile(cls, fileName):
        loadedPopulation = cls()
        with open(fileName, 'rb') as file:
            loadedPopulation.agentList = pickle.load(file)
        return loadedPopulation