from framework import (Framework, main)
from math import cos
from Box2D import *
from walker import Walker
from networks.network import Network
from evolution.population import Population
from evolution import selection
from learningSettings import learningSettings


class Simulator(Framework):
    name = "Simulator"

    def __init__(self, showGraphics = True):
        self.showGraphics = showGraphics
        if(showGraphics):
            super(Simulator, self).__init__()
        else:
            self.world = b2World(gravity=(0, -10), doSleep=True)
            self.stepCount = 0

        self.resultsFile = open('results/Test.txt', 'w')

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

        #Every second, add each agent's state to its history
        if (self.stepCount % settings.hz) == 0:
            for i in range(len(self.population.agentList)):
                self.population.agentList[i].addToHistory(self.walkerList[i].getJointAngles())

        #Deal with the end of a trial
        if (self.stepCount % (learningSettings.secondsPerTrial * settings.hz)) == 0:
            self.population.calculateFitness(self.walkerList, learningSettings.selectionCriteria)
            #Print the average and highest positions
            positionSum = 0
            highestPosition = -90
            for walker in self.walkerList:
                walkerPosition = walker.getTorsoPosition()[0]
                positionSum += walkerPosition
                highestPosition = max(highestPosition, walkerPosition)
            self.resultsFile.write(str((int) (self.stepCount / (learningSettings.secondsPerTrial * settings.hz))) + ',' + str(positionSum / len(self.walkerList)) + ',' + str(highestPosition) + '\n')
            #Make the next population
            print(str((int) (self.stepCount / (learningSettings.secondsPerTrial * settings.hz))) + ": ", end="")
            self.population = self.population.makeNextPopulation(self.walkerList, learningSettings.selectionCriteria)
            for walker in self.walkerList:
                walker.resetPosition()


        if (self.stepCount == learningSettings.secondsPerTrial * settings.hz * learningSettings.numberOfTrials):
            self.resultsFile.close()
            exit()



if __name__ == "__main__":
    main(Simulator)
