from framework import (Framework, main)
from Box2D import *
from walker import Walker
from networks.network import Network
from evolution.population import Population
from evolution import selection, speciation
from learningSettings import learningSettings
from fileHandling import fileHandler


class Simulator(Framework):
    name = "Simulator"
    experimentCount = 0

    def __init__(self, showGraphics = True):
        self.showGraphics = showGraphics
        if(showGraphics):
            super(Simulator, self).__init__()
        else:
            self.world = b2World(gravity=(0, -10), doSleep=True)
            self.stepCount = 0

        self.fileHandler = fileHandler(learningSettings.fileName)

        self.secondsElapsed = 0
        self.groupsElapsed = 0
        self.generationsElapsed = 0

        self.Setup()

    def Setup(self):
        #Create the ground
        self.world.CreateStaticBody(position=(0, -10), shapes=b2PolygonShape(box=(10000, 10)))

        #Make some walkers
        self.walkerList = []
        for i in range(learningSettings.walkerCount):
            self.walkerList.append(Walker(self.world, i*10, learningSettings.useSimpleWalkers))

        #Make a population of agents
        jointCount = len(self.walkerList[0].jointList)
        sampleNetwork = Network(jointCount + 2, jointCount, [jointCount])
        self.population = Population(learningSettings.walkerCount, sampleNetwork)

        #If we need it, setup an environment for speciation
        if(learningSettings.selectionCriteria == selection.SPECIATION):
            self.environment = speciation.Environment()
            self.environment.generateAllFood(self.walkerList[0],
                                             learningSettings.foodCount,
                                             learningSettings.foodUses,
                                             learningSettings.foodEnergy)

    def Step(self, settings):
        if(self.showGraphics):
            super(Simulator, self).Step(settings)
        else:
            self.stepCount += 1
            self.world.Step(1 / settings.hz, settings.velocityIterations, settings.positionIterations)
            self.world.ClearForces()

        #If everyone has died, stop the experiment
        if(self.population.size() == 0):
            print("All agents have died.")
            self.afterExperiment(settings)
            return

        #Advance all walkers
        for i in range(len(self.walkerList)):
            agent = self.findAgentForWalker(i, learningSettings.groupSize)
            # If we had extra walkers, don't try to deal with their agents
            if (agent is None):
                break

            walker = self.walkerList[i]
            #Angle and height of torso
            input = [walker.getTorsoAngle(), walker.getTorsoPosition()[1] / 10.0]
            input.extend(walker.getJointAngles())

            network = agent.network
            networkOutput = network.Feedforwad(input)
            jointForces = [(i - .5)*25 for i in networkOutput]
            walker.setJointForces(jointForces)

        #Do this every second
        if (self.stepCount % settings.hz) == 0:
            self.afterSecond(settings, learningSettings.groupSize)

        #Deal with the end of a group
        if (self.secondsElapsed == learningSettings.secondsPerRun):
            self.afterGroup(settings, learningSettings.groupSize)

        #Deal with the end of a generation
        if (self.groupsElapsed * learningSettings.groupSize >= self.population.size()):
            self.afterGeneration(settings)
            print(self.population.size())

        #Deal with end of experiment
        if (self.generationsElapsed == learningSettings.numberOfGenerations):
            self.afterExperiment(settings)

    #What to do each second
    def afterSecond(self, settings, groupSize):
        #Add each walker's state to its agent's history
        for i in range(len(self.walkerList)):
            agent = self.findAgentForWalker(i, groupSize)
            #If we had extra walkers, don't try to deal with their agents
            if(agent is None):
                break
            agent.addToHistory(self.walkerList[i].getJointAngles())
        self.secondsElapsed += 1

    #What to do after each group
    def afterGroup(self, settings, groupSize):
        for i in range(len(self.walkerList)):
            agent = self.findAgentForWalker(i, groupSize)
            #If we had extra walkers, don't try to deal with their agents
            if(agent is None):
                break
            agent.fitness = self.walkerList[i].getTorsoPosition()[0] - self.walkerList[i].startingXOffset
        self.groupsElapsed += 1
        self.secondsElapsed = 0

    #What to do each generation
    def afterGeneration(self, settings):
        #Calculate the fitness for everyone
        print(str(self.generationsElapsed) + ": ", end="")
        self.population.calculateFitness(learningSettings.selectionCriteria)
        #Print the average and best positions
        averageAndBestPositions = self.getAverageAndBestPositions()
        averagePosition = averageAndBestPositions[0]
        bestPosition = averageAndBestPositions[1]
        self.fileHandler.write(str(self.generationsElapsed) + ',' + str(averagePosition) + ',' + str(bestPosition) + '\n')
        #Make the next generation
        if(learningSettings.selectionCriteria != selection.SPECIATION):
            self.population = self.population.makeNextPopulation(self.walkerList, learningSettings.selectionCriteria)
        else:
            if((self.generationsElapsed + 1) % learningSettings.runsBetweenBreeding == 0):
                self.population = self.environment.generateNextPopulation(self.population)
            else:
                for agent in self.population.agentList:
                    agent.resetHistory()
            if(learningSettings.staticFood):
                self.environment.refillAllFood()
            else:
                self.environment.generateAllFood(self.walkerList[0],
                                                 learningSettings.foodCount,
                                                 learningSettings.foodUses,
                                                 learningSettings.foodEnergy)
        self.updateWalkers()
        self.generationsElapsed += 1
        self.groupsElapsed = 0


    #What to do at the end of the experiment
    def afterExperiment(self, settings):
        Simulator.experimentCount += 1
        if(Simulator.experimentCount >= learningSettings.numberOfExperiments):
            exit()
        else:
            self.__init__(False)

    #Find the agent currently driving this walker for this group
    def findAgentForWalker(self, walkerIndex, groupSize):
        agentIndex = self.groupsElapsed * groupSize + walkerIndex
        #If the walker wasn't actually being driven by anything, return None
        if(agentIndex >= self.population.size()):
            return None
        return self.population.agentList[agentIndex]

    def getAverageAndBestPositions(self):
        positionSum = 0
        bestPosition = -90
        for walker in self.walkerList:
            walkerPosition = walker.getTorsoPosition()[0]
            positionSum += walkerPosition
            bestPosition = max(bestPosition, walkerPosition)
        averagePosition = positionSum / len(self.walkerList)
        return (averagePosition, bestPosition)

    def updateWalkers(self):
        popSize = self.population.size()
        #If there's more walkers than agents, remove the extra walkers
        while(len(self.walkerList) > popSize):
            self.walkerList[-1].removeWalker(self.world)
            del(self.walkerList[-1])
        #Reset all walkers
        for walker in self.walkerList:
            walker.resetPosition()
        #If we need more walkers, add them now
        if(len(self.walkerList) < popSize):
            for i in range(popSize - len(self.walkerList)):
                self.walkerList.append(Walker(self.world, learningSettings.useSimpleWalkers))



if __name__ == "__main__":
    main(Simulator)
