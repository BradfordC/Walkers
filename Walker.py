from Box2D import *


class Walker:
    BODY_HEAD = 0
    BODY_TORSO = 1
    BODY_ARM1_UPPER = 2
    BODY_ARM1_LOWER = 3
    BODY_ARM2_UPPER = 4
    BODY_ARM2_LOWER = 5
    BODY_LEG1_UPPER = 6
    BODY_LEG1_LOWER = 7
    BODY_LEG1_FOOT = 8
    BODY_LEG2_UPPER = 9
    BODY_LEG2_LOWER = 10
    BODY_LEG2_FOOT = 11

    JOINT_NECK = 0
    JOINT_ARM1_SHOULDER = 1
    JOINT_ARM1_ELBOW = 2
    JOINT_ARM2_SHOULDER = 3
    JOINT_ARM2_ELBOW = 4
    JOINT_LEG1_HIP = 5
    JOINT_LEG1_KNEE = 6
    JOINT_LEG1_ANKLE = 7
    JOINT_LEG2_HIP = 8
    JOINT_LEG2_KNEE = 9
    JOINT_LEG2_ANKLE = 10

    def __init__(self, world):
        self.bodyList = [None] * 12
        self.positionList = [None] * 12
        self.jointList = [None] * 11

        #Head
        self.__addBodyPart(world, (1.0,1.0), (0, 13), Walker.BODY_HEAD)
        #Torso
        self.__addBodyPart(world, (1, 2.5), (0, 9.5), Walker.BODY_TORSO, Walker.BODY_HEAD, Walker.JOINT_NECK, (-45, 45))
        #Arm 1
        self.__addBodyPart(world, (.35, 1.25), (0, 10.75), Walker.BODY_ARM1_UPPER, Walker.BODY_TORSO, Walker.JOINT_ARM1_SHOULDER, (-90, 90))
        self.__addBodyPart(world, (.35, 1.25), (0, 8.25), Walker.BODY_ARM1_LOWER, Walker.BODY_ARM1_UPPER, Walker.JOINT_ARM1_ELBOW, (0, 90))
        #Arm 2
        self.__addBodyPart(world, (.35, 1.25), (0, 10.75), Walker.BODY_ARM2_UPPER, Walker.BODY_TORSO, Walker.JOINT_ARM2_SHOULDER, (-90, 90))
        self.__addBodyPart(world, (.35, 1.25), (0, 8.25), Walker.BODY_ARM2_LOWER, Walker.BODY_ARM2_UPPER, Walker.JOINT_ARM2_ELBOW, (0, 90))
        #Leg 1
        self.__addBodyPart(world, (.5, 1.5), (0, 5.5), Walker.BODY_LEG1_UPPER, Walker.BODY_TORSO, Walker.JOINT_LEG1_HIP, (-45, 90))
        self.__addBodyPart(world, (.5, 1.5), (0, 2.5), Walker.BODY_LEG1_LOWER, Walker.BODY_LEG1_UPPER, Walker.JOINT_LEG1_KNEE, (-90, 0))
        self.__addBodyPart(world, (1, .25), (0.5, .75), Walker.BODY_LEG1_FOOT, Walker.BODY_LEG1_LOWER, Walker.JOINT_LEG1_ANKLE, (-45, 45), (-.5, 0))
        #Leg 2
        self.__addBodyPart(world, (.5, 1.5), (0, 5.5), Walker.BODY_LEG2_UPPER, Walker.BODY_TORSO, Walker.JOINT_LEG2_HIP, (-45, 90))
        self.__addBodyPart(world, (.5, 1.5), (0, 2.5), Walker.BODY_LEG2_LOWER, Walker.BODY_LEG2_UPPER, Walker.JOINT_LEG2_KNEE, (-90, 0))
        self.__addBodyPart(world, (1, .25), (0.5, .75), Walker.BODY_LEG2_FOOT, Walker.BODY_LEG2_LOWER, Walker.JOINT_LEG2_ANKLE, (-45, 45), (-.5, 0))

        self.resetPosition()

    def __addBodyPart(self, world, box, position, bodyIndex, connectedBodyIndex = -1, jointIndex = -1, jointLimits = (0, 0), jointOffset=(0,0)):
        self.positionList[bodyIndex] = position
        body = world.CreateDynamicBody(position=position)
        body.CreatePolygonFixture(box=box, density=1, friction=0.3, filter=b2Filter(groupIndex = -1))
        self.bodyList[bodyIndex] = body
        if(connectedBodyIndex >= 0):
            #Connect the joint at the top middle of this object, plus any offset
            joint = world.CreateRevoluteJoint(bodyA=self.bodyList[connectedBodyIndex],
                                              bodyB=body,
                                              anchor=(position[0] + jointOffset[0], position[1] + box[1] + jointOffset[1]),
                                              lowerAngle =jointLimits[0] / 180 * b2_pi,  #Convert degrees to radians
                                              upperAngle =jointLimits[1] / 180 * b2_pi,  #Convert degrees to radians
                                              enableLimit = True,
                                              maxMotorTorque = 100.0,
                                              enableMotor = True)
            self.jointList[jointIndex] = joint

    def getJointAngles(self):
        jointAngles = []
        for joint in self.jointList:
            jointAngles.append(joint.angle)
        return jointAngles

    def setJointForces(self, forces):
        if(len(forces) == len(self.jointList)):
            for i in range(len(forces)):
                self.jointList[i].motorSpeed = forces[i]
        else:
            print("ERROR: Size mismatch in setting joint forces.")

    def getTorsoPosition(self):
        return self.bodyList[Walker.BODY_TORSO].position[0]

    def resetPosition(self):
        for i in range(len(self.bodyList)):
            body = self.bodyList[i]
            body.transform = [self.positionList[i], 0]
            body.linearVelocity = (0, 0)
            body.angularVelocity = 0

        #Move the arms and legs slightly so that they diverge from the start
        self.bodyList[Walker.BODY_LEG1_UPPER].angularVelocity = 5
        self.bodyList[Walker.BODY_LEG2_UPPER].angularVelocity = -5
        self.bodyList[Walker.BODY_ARM1_UPPER].angularVelocity = 5
        self.bodyList[Walker.BODY_ARM2_UPPER].angularVelocity = -5

