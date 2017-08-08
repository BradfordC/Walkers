from evolution import population
from learningSettings import learningSettings
import random

class Environment:

    def __init__(self):
        self.foodList = []

    #Have all current agents attempt to eat and mate, passing themselves to the next generation as well if they survive
    def generateNextPopulation(self, oldPopulation):
        breedingPopulation = population()
        newPopulation = population()

        oldPopulation.sortByFitness()
        #Feed
        for agent in oldPopulation.agentList:
            #Look for food that it can eat
            ateFood = False
            for food in self.foodList:
                if(agent.eatFood(food)):
                    ateFood = True
                    break
            if(not ateFood):
                agent.energy = agent.energy - 1
        #Migrate any agents that survived
        for agent in oldPopulation.agentList:
            if(agent.energy > 0):
                breedingPopulation.agentList.append(agent)
                newPopulation.agentList.append(agent)
        #Find mates and add the offspring to the final population
        popSize = len(breedingPopulation.agentList)
        random.shuffle(breedingPopulation.agentList)
        for i in range(popSize):
            agent = breedingPopulation.agentList[i]
            #Find a random mate that is compatible
            startIndex = random.randint(0, popSize)
            #Make sure we don't start with ourselves
            if(startIndex == i):
                startIndex = startIndex + 1
            pairIndex = startIndex
            while True:
                #Don't mate with itself
                if(pairIndex == i):
                    continue
                #Try to mate
                if(agent.getHistoryDistance(breedingPopulation.agentList[pairIndex]) < learningSettings.choosinessLimit):
                    newPopulation.agentList.append(agent.cross(breedingPopulation.agentList[pairIndex]))
                    break
                #Go to the next potential mate
                pairIndex = (pairIndex + 1)%popSize
                #If we've checked all mates, then give up
                if(pairIndex == startIndex):
                    break

        return newPopulation

    def generateFood(sampleWalker, arraySize):
        food = []
        for i in range(arraySize):
            food.append(sampleWalker.getRandomJointAngles())
        return food

class Food:
    def __init__(self, history, uses, value):
        self.history = history
        self.maxUses = uses
        self.remainingUses = uses
        self.value = value

    #See if the agent is able to eat this food
    def canBeEaten(self, agent):
        return (self.remainingUses > 0) and (agent.getHistoryDistance(self.history) < learningSettings.choosinessLimit)

    def refill(self):
        self.remainingUses = self.maxUses