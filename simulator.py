import learningSettings
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
        self.agentsEvaluated = 0

        self.Setup()

    def Setup(self):
        #Create the ground
        self.world.CreateStaticBody(position=(0, -10), shapes=b2PolygonShape(box=(10000, 10)))

        #Make some walkers
        self.walkerList = []
        for i in range(learningSettings.groupSize):
            self.walkerList.append(Walker(self.world, (i*10, 0), learningSettings.useSimpleWalkers))

        #Make a population of agents
        if(learningSettings.loadPopulation):
            self.population = Population.loadFromFile(learningSettings.populationFile)
        else:
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
            jointForces = [(i - .5)*100 for i in networkOutput]
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
            walker = self.walkerList[i]
            #If we had extra walkers, don't try to deal with their agents
            if(agent is None):
                break
            agent.addToHistory(walker.getTorsoPosition(), walker.getJointAngles())
        self.secondsElapsed += 1

    #What to do after each group
    def afterGroup(self, settings, groupSize):
        self.resetWalkers()
        self.groupsElapsed += 1
        self.secondsElapsed = 0

    #What to do each generation
    def afterGeneration(self, settings):
        #Calculate the fitness for everyone
        print(str(self.generationsElapsed) + ": ", end="")
        self.population.setNovelty()
        self.population.printScore(learningSettings.selectionCriteria)
        #Print the average and best positions
        averageAndBestFitness = self.getAverageAndBestFitness()
        averageFitness = averageAndBestFitness[0]
        bestFitness = averageAndBestFitness[1]
        self.agentsEvaluated += self.population.size()
        self.fileHandler.write(str(self.agentsEvaluated) + ',' + str(averageFitness) + ',' + str(bestFitness) + '\n')
        #Make the next generation
        if(learningSettings.selectionCriteria != selection.SPECIATION):
            self.population = self.population.makeNextPopulation(learningSettings.selectionCriteria)
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
        self.generationsElapsed += 1
        self.groupsElapsed = 0


    #What to do at the end of the experiment
    def afterExperiment(self, settings):
        Simulator.experimentCount += 1
        self.population.saveToFile(self.fileHandler.popSaveName)
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

    def getAverageAndBestFitness(self):
        fitnessSum = 0
        bestFitness = -90
        for agent in self.population.agentList:
            fitnessSum += agent.performance.getFitness()
            bestFitness = max(bestFitness, agent.performance.getFitness())
        averageFitness = fitnessSum / self.population.size()
        return (averageFitness, bestFitness)

    def resetWalkers(self):
        #Reset all walkers
        for walker in self.walkerList:
            walker.resetPosition()



if __name__ == "__main__":
    main(Simulator)
