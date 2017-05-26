from .framework import (Framework, main)
from math import cos
from Box2D import *
from Walker import Walker
from Networks import Network


class Simulator(Framework):
    name = "Simulator"

    def __init__(self):
        super(Simulator, self).__init__()

        self.world.CreateStaticBody(position=(0, -10), shapes=b2PolygonShape(box=(50, 10)))

        self.walker = Walker(self.world)
        self.secondsPerTrial = 5

        jointCount = len(self.walker.jointList)
        self.network = Network.Network(jointCount, jointCount, [jointCount])



    def Step(self, settings):
        super(Simulator, self).Step(settings)

        output = self.network.Feedforwad(self.walker.getJointAngles())
        forces = [(i - .5)*10 for i in output]
        self.walker.setJointForces(forces)

        if (self.stepCount % (self.secondsPerTrial * 60)) == 0:
            print(self.walker.getTorsoPosition())
            self.walker.resetPosition()
            jointCount = len(self.walker.jointList)
            self.network = Network.Network(jointCount, jointCount, [jointCount])
            print(forces)


if __name__ == "__main__":
    main(Simulator)
