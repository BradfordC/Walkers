from .framework import (Framework, main)
from math import cos
from Box2D import *
from Walker import Walker
from Networks.Network import Network
from Evolution.Population import Population


class Simulator(Framework):
    name = "Simulator"

    def __init__(self):
        super(Simulator, self).__init__()
        #Create the ground
        self.world.CreateStaticBody(position=(0, -10), shapes=b2PolygonShape(box=(50, 10)))

        self.secondsPerTrial = 15
        self.walkerCount = 40

        #Make some walkers
        self.walkerList = []
        for i in range(self.walkerCount):
            self.walkerList.append(Walker(self.world))

        #Make a population of agents
        jointCount = len(self.walkerList[0].jointList)
        sampleNetwork = Network(jointCount, jointCount, [jointCount])
        self.population = Population(self.walkerCount, sampleNetwork)

    def Step(self, settings):
        super(Simulator, self).Step(settings)

        #Advance all walkers
        for i in range(self.walkerCount):
            walker = self.walkerList[i]
            network = self.population.agentList[i].network
            networkOutput = network.Feedforwad(walker.getJointAngles())
            jointForces = [(i - .5)*10 for i in networkOutput]
            walker.setJointForces(jointForces)

        #Deal with the end of a trial
        if (self.stepCount % (self.secondsPerTrial * 60)) == 0:
            for i in range(self.walkerCount):
                walker = self.walkerList[i]
                self.population.agentList[i].fitness = walker.getTorsoPosition();
                walker.resetPosition()

            print(self.population.getHighestFitness())
            self.population = self.population.makeNextPopulation()

        if (self.stepCount == self.secondsPerTrial * 60 * 1000):
            exit()



if __name__ == "__main__":
    main(Simulator)
