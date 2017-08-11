from evolution import population
from learningSettings import learningSettings
import random

class Environment:
    def __init__(self):
        self.foodList = []

    #Have all current agents attempt to eat and mate, passing themselves to the next generation as well if they survive
    def generateNextPopulation(self, oldPopulation):
        breedingPopulation = population.Population()
        newPopulation = population.Population()

        oldPopulation.sortByFitness()
        #Feed
        sum = 0
        maxA = 0
        for agent in oldPopulation.agentList:
            avgDist = self.tryToFeed(agent)
            sum += avgDist
            maxA = max(maxA, avgDist)
        print(sum / len(oldPopulation.agentList))
        print(maxA)
        sum = 0
        for i in range(len(oldPopulation.agentList)):
            for j in range(i + 1, len(oldPopulation.agentList)):
                sum += 2 * oldPopulation.agentList[i].getHistoryDistance(oldPopulation.agentList[j].history)
        print((sum / len(oldPopulation.agentList)/len(oldPopulation.agentList)))
        print()
        #Migrate any agents that survived
        for agent in oldPopulation.agentList:
            if(agent.energy > 0):
                breedingPopulation.agentList.append(agent)
                newPopulation.agentList.append(agent)
        #Find mates and add the offspring to the final population
        popSize = len(breedingPopulation.agentList)
        if(popSize > 1):
            random.shuffle(breedingPopulation.agentList)
            for i in range(popSize):
                agent = breedingPopulation.agentList[i]
                #Find a random mate that is compatible
                startIndex = random.randint(0, popSize - 1) #Randint is inclusive
                #Make sure we don't start with ourselves
                if(startIndex == i):
                    startIndex = (startIndex + 1)%popSize
                pairIndex = startIndex
                while True:
                    #Don't mate with itself
                    if(pairIndex == i):
                        pairIndex = (pairIndex + 1)%popSize
                        continue
                    #Try to mate
                    if(agent.getHistoryDistance(breedingPopulation.agentList[pairIndex].history) < learningSettings.choosinessLimitMate):
                        newPopulation.agentList.append(agent.cross(breedingPopulation.agentList[pairIndex]))
                        break
                    #If we've checked all mates, then give up
                    if(pairIndex == startIndex):
                        break
                    #Go to the next potential mate
                    pairIndex = (pairIndex + 1)%popSize
        #Remove the history of old agents
        for agent in breedingPopulation.agentList:
            agent.resetHistory()

        return newPopulation

    #Have the agent try to eat some food
    def tryToFeed(self, agent):
        #Look for food that it can eat
        ateFood = False
        sumDistance = 0
        for food in self.foodList:
            if(agent.eatFood(food)):
                ateFood = True
                break
        if(not ateFood):
            agent.energy = agent.energy - 1

        for food in self.foodList:
            sumDistance += agent.getHistoryDistance(food.history)
        return sumDistance / len(self.foodList)

    #Create a single instance of food
    def generateSingleFood(sampleWalker, arraySize):
        food = []
        for i in range(arraySize):
            food.append(sampleWalker.getRandomJointAngles())
        return food

    #Create new food with random histories
    def generateAllFood(self, sampleWalker, foodCount, foodUses, foodEnergy):
        self.foodList = []
        for i in range(foodCount):
            self.foodList.append(Food(
                Environment.generateSingleFood(sampleWalker, learningSettings.secondsPerRun),
                foodUses,
                foodEnergy
            ))

    #Refill current food and keep histories
    def refillAllFood(self):
        for food in self.foodList:
            food.refill()

class Food:
    def __init__(self, history, uses, energy):
        self.history = history
        self.maxUses = uses
        self.remainingUses = uses
        self.energy = energy

    #See if the agent is able to eat this food
    def canBeEaten(self, agent):
        return (self.remainingUses > 0) and (agent.getHistoryDistance(self.history) < learningSettings.choosinessLimitFood)

    def refill(self):
        self.remainingUses = self.maxUses