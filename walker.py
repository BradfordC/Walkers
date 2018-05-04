from Box2D import *
import random


class Walker:
    def __init__(self, world, startingOffset, isSimple=False):
        self.bodyList = []
        self.positionList = []
        self.jointList = []
        self.jointLimits = []

        #Include an offset so that walkers don't overlap, which speeds things up
        self.startingOffset = startingOffset

        #Keep track of the torso index, to attach body parts to it and to be able to track its position during the test
        self.torsoIndex = -1
        self.headIndex = -1

        if(isSimple):
            #No head or arms, just the torso
            self.__addBodyPart(world, (1, 2.5), (0, 9.5))
            torsoIndex = len(self.bodyList) - 1
        else:
            #Head
            self.__addBodyPart(world, (1.0,1.0), (0, 13))
            self.headIndex = len(self.bodyList) - 1
            #Torso
            self.__addBodyPart(world, (1, 2.5), (0, 9.5), len(self.bodyList) - 1, (-45, 45))
            torsoIndex = len(self.bodyList) - 1
            #Arm 1
            self.__addBodyPart(world, (.35, 1.25), (0, 10.75), len(self.bodyList) - 1, (-90, 90))
            self.__addBodyPart(world, (.35, 1.25), (0, 8.25), len(self.bodyList) - 1, (0, 90))
            #Arm 2
            self.__addBodyPart(world, (.35, 1.25), (0, 10.75), torsoIndex, (-90, 90))
            self.__addBodyPart(world, (.35, 1.25), (0, 8.25), len(self.bodyList) - 1, (0, 90))
        #Leg 1
        self.__addBodyPart(world, (.5, 1.5), (0, 5.5), torsoIndex, (-45, 90))
        self.__addBodyPart(world, (.5, 1.5), (0, 2.5), len(self.bodyList) - 1, (-90, 0))
        self.__addBodyPart(world, (1, .25), (0.25, .75), len(self.bodyList) - 1, (-45, 45), (-.25, 0))
        #Leg 2
        self.__addBodyPart(world, (.5, 1.5), (0, 5.5), torsoIndex, (-45, 90))
        self.__addBodyPart(world, (.5, 1.5), (0, 2.5), len(self.bodyList) - 1, (-90, 0))
        self.__addBodyPart(world, (1, .25), (0.25, .75), len(self.bodyList) - 1, (-45, 45), (-.25, 0))

        self.resetPosition()

    def __addBodyPart(self, world, box, position, connectedBodyIndex=-1, jointLimits = (0, 0), jointOffset=(0,0)):
        self.positionList.append(position)
        body = world.CreateDynamicBody(position=position)
        body.CreatePolygonFixture(box=box, density=5, friction=.9, filter=b2Filter(groupIndex = -1))
        self.bodyList.append(body)
        if(connectedBodyIndex >= 0):
            #Connect the joint at the top middle of this object, plus any offset
            lowerLimit = jointLimits[0] / 180 * b2_pi  #Convert degrees to radians
            upperLimit = jointLimits[1] / 180 * b2_pi  #Convert degrees to radians
            joint = world.CreateRevoluteJoint(bodyA=self.bodyList[connectedBodyIndex],
                                              bodyB=body,
                                              anchor=(position[0] + jointOffset[0], position[1] + box[1] + jointOffset[1]),
                                              lowerAngle = lowerLimit,
                                              upperAngle = upperLimit,
                                              enableLimit = True,
                                              maxMotorTorque = 500.0,
                                              enableMotor = True)
            self.jointList.append(joint)
            self.jointLimits.append((lowerLimit, upperLimit))

    #Remove the walker from the world
    def removeWalker(self, world):
        for body in self.bodyList:
            world.DestroyBody(body)

    #Get an array of the current joint angles
    def getJointAngles(self):
        jointAngles = []
        for joint in self.jointList:
            jointAngles.append(joint.angle)
        return jointAngles

    #Get an array of random possible joint angles
    def getRandomJointAngles(self):
        jointAngles = []
        for i in range(len(self.jointList)):
            joint = self.jointList[i]
            jointAngles.append(random.uniform(self.jointLimits[i][0], self.jointLimits[i][1]))
        return jointAngles

    #Set the forces on the joints
    def setJointForces(self, forces):
        if(len(forces) == len(self.jointList)):
            for i in range(len(forces)):
                self.jointList[i].motorSpeed = forces[i]
        else:
            print("ERROR: Size mismatch in setting joint forces.")

    def getHeadPosition(self):
        if(self.headIndex == -1):
            return self.getTorsoPosition()
        else:
            position = self.bodyList[self.headIndex].position
            return (position[0] - self.startingOffset, position[1] - self.startingOffset[1])

    def getTorsoPosition(self):
        #Turn the position into a regular tuple
        position = self.bodyList[self.torsoIndex].position
        return (position[0] - self.startingOffset[0], position[1] - self.startingOffset[1])

    def getTorsoAngle(self):
        return self.bodyList[self.torsoIndex].angle

    def resetPosition(self):
        for i in range(len(self.bodyList)):
            body = self.bodyList[i]

            adjustedPosition = [self.positionList[i][0] + self.startingOffset[0], self.positionList[i][1] + self.startingOffset[1]]

            body.transform = [adjustedPosition, 0]
            body.linearVelocity = (0, 0)
            body.angularVelocity = 0

