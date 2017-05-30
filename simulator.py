from framework import (Framework, main)
from math import cos
from Box2D import *
from walker import Walker
from networks.network import Network
from evolution.population import Population


class Simulator(Framework):
    name = "Simulator"

    def __init__(self, showGraphics = True):
        self.showGraphics = showGraphics
        if(showGraphics):
            super(Simulator, self).__init__()
        else:
            self.world = b2World(gravity=(0, -10), doSleep=True)
            self.stepCount = 0

        self.Setup()

    def Setup(self):
        #Create the ground
        self.world.CreateStaticBody(position=(0, -10), shapes=b2PolygonShape(box=(50, 10)))

        self.secondsPerTrial = 5
        self.walkerCount = 100

        #Make some walkers
        self.walkerList = []
        for i in range(self.walkerCount):
            self.walkerList.append(Walker(self.world, False))

        #Make a population of agents
        jointCount = len(self.walkerList[0].jointList)
        sampleNetwork = Network(jointCount + 2, jointCount, [jointCount])
        self.population = Population(self.walkerCount, sampleNetwork)

    def Step(self, settings):
        if(self.showGraphics):
            super(Simulator, self).Step(settings)
        else:
            self.stepCount += 1
            self.world.Step(1 / settings.hz, settings.velocityIterations, settings.positionIterations)
            self.world.ClearForces()

        #Advance all walkers
        for i in range(self.walkerCount):
            walker = self.walkerList[i]
            #Angle and height of torso
            input = [walker.getTorsoAngle(), walker.getTorsoPosition()[1] / 10.0]
            input.extend(walker.getJointAngles())

            network = self.population.agentList[i].network
            networkOutput = network.Feedforwad(input)
            jointForces = [(i - .5)*25 for i in networkOutput]
            walker.setJointForces(jointForces)

        #Deal with the end of a trial
        if (self.stepCount % (self.secondsPerTrial * 60)) == 0:
            for i in range(self.walkerCount):
                walker = self.walkerList[i]
                self.population.agentList[i].fitness = walker.getTorsoPosition()[0] + walker.getTorsoPosition()[1];
                walker.resetPosition()

            print(self.population.getHighestFitness())
            self.population = self.population.makeNextPopulation()

        if (self.stepCount == self.secondsPerTrial * 60 * 10000):
            exit()



if __name__ == "__main__":
    main(Simulator)
