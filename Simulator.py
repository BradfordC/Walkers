from .framework import (Framework, main)
from math import cos
from Box2D import *
from Walker import Walker


class Simulator(Framework):
    name = "Simulator"

    def __init__(self):
        super(Simulator, self).__init__()

        self.world.CreateStaticBody(position=(0, -10), shapes=b2PolygonShape(box=(50, 10)))

        self.walker = Walker(self.world)
        self.secondsPerTrial = 5

    def Step(self, settings):
        super(Simulator, self).Step(settings)

        force = cos(self.stepCount / (self.secondsPerTrial * 60) * 2 * b2_pi) * 2
        self.walker.setJointForces((force,) * 11)

        if (self.stepCount % (self.secondsPerTrial * 60)) == 0:
            print(self.walker.getTorsoPosition())
            self.walker.resetPosition()


if __name__ == "__main__":
    main(Simulator)
