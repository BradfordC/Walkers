from framework import (Framework, main)
from Box2D import *
from walker import Walker
from networks.network import Network
from evolution.population import Population
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

        self.Setup()

    def Setup(self):
        #Create the ground
        self.world.CreateStaticBody(position=(0, -10), shapes=b2PolygonShape(box=(50, 10)))

        #Make some walkers
        self.walkerList = []
        for i in range(learningSettings.walkerCount):
            self.walkerList.append(Walker(self.world, False))

        #Make a population of agents
        jointCount = len(self.walkerList[0].jointList)
        sampleNetwork = Network(jointCount + 2, jointCount, [jointCount])
        self.population = Population(learningSettings.walkerCount, sampleNetwork)

    def Step(self, settings):
        if(self.showGraphics):
            super(Simulator, self).Step(settings)
        else:
            self.stepCount += 1
            self.world.Step(1 / settings.hz, settings.velocityIterations, settings.positionIterations)
            self.world.ClearForces()

        #Advance all walkers
        for i in range(learningSettings.walkerCount):
            walker = self.walkerList[i]
            #Angle and height of torso
            input = [walker.getTorsoAngle(), walker.getTorsoPosition()[1] / 10.0]
            input.extend(walker.getJointAngles())

            network = self.population.agentList[i].network
            networkOutput = network.Feedforwad(input)
            jointForces = [(i - .5)*25 for i in networkOutput]
            walker.setJointForces(jointForces)

        #Do this every second
        if (self.stepCount % settings.hz) == 0:
            self.afterSecond(settings)

        #Deal with the end of a generation
        if (self.stepCount % (learningSettings.secondsPerRun * settings.hz)) == 0:
            self.afterGeneration(settings)

        #Deal with end of experiment
        if (self.stepCount == learningSettings.secondsPerRun * settings.hz * learningSettings.numberOfGenerations):
            self.afterExperiment(settings)

    #What to do each second
    def afterSecond(self, settings):
        #Add each agent's state to its history
        for i in range(len(self.population.agentList)):
            self.population.agentList[i].addToHistory(self.walkerList[i].getJointAngles())

    #What to do each generation
    def afterGeneration(self, settings):
        print(str((int) (self.stepCount / (learningSettings.secondsPerRun * settings.hz))) + ": ", end="")
        self.population.calculateFitness(self.walkerList, learningSettings.selectionCriteria)
        print(len(self.population.agentList[0].history))
        #Print the average and highest positions
        positionSum = 0
        highestPosition = -90
        for walker in self.walkerList:
            walkerPosition = walker.getTorsoPosition()[0]
            positionSum += walkerPosition
            highestPosition = max(highestPosition, walkerPosition)
        self.fileHandler.write(str((int) (self.stepCount / (learningSettings.secondsPerRun * settings.hz))) + ',' + str(positionSum / len(self.walkerList)) + ',' + str(highestPosition) + '\n')
        #Make the next generation
        self.population = self.population.makeNextPopulation(self.walkerList, learningSettings.selectionCriteria)
        for walker in self.walkerList:
            walker.resetPosition()

    #What to do at the end of the experiment
    def afterExperiment(self, settings):
        Simulator.experimentCount += 1
        if(Simulator.experimentCount >= learningSettings.numberOfExperiments):
            exit()
        else:
            self.__init__(False)

if __name__ == "__main__":
    main(Simulator)
