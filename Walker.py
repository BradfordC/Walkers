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
    JOINT_LEG1_FOOT = 7
    JOINT_LEG2_HIP = 8
    JOINT_LEG2_KNEE = 9
    JOINT_LEG2_FOOT = 10

    def __init__(self, world):
        self.bodyList = [] * 12
        self.positionList = [] * 12
        self.jointList = [] * 11

        headTop = 14
        headBox = (1.0, 1.0)
        self.headPosition = (0, headTop - headBox[1])
        self.headBody = world.CreateDynamicBody(position=self.headPosition)
        head = self.headBody.CreatePolygonFixture(box=headBox, density=1, friction=0.3, filter=b2Filter(groupIndex=-1))

        maxMotorTorque = 100.0

        torsoTop = headTop - headBox[1] * 2
        torsoBox = (1, 2.5)
        self.torsoPosition = (0, torsoTop - torsoBox[1])
        self.torsoBody = world.CreateDynamicBody(position=self.torsoPosition)
        torso = self.torsoBody.CreatePolygonFixture(box=torsoBox, density=1, friction=0.3,
                                                    filter=b2Filter(groupIndex=-1))
        self.neckJoint = world.CreateRevoluteJoint(bodyA=self.headBody,
                                                   bodyB=self.torsoBody,
                                                   anchor=(0, torsoTop),
                                                   lowerAngle=-.25 * b2_pi,  # -45 degrees
                                                   upperAngle=.25 * b2_pi,  # 45 degrees
                                                   enableLimit=True,
                                                   maxMotorTorque=maxMotorTorque,
                                                   enableMotor=True)

        upperArm1Top = torsoTop
        upperArm1Box = (.35, 1.25)
        self.upperArm1Position = (0, upperArm1Top - upperArm1Box[1])
        self.upperArm1Body = world.CreateDynamicBody(position=self.upperArm1Position)
        upperArm1 = self.upperArm1Body.CreatePolygonFixture(box=upperArm1Box, density=1, friction=0.3,
                                                       filter=b2Filter(groupIndex=-1))
        self.shoulder1Joint = world.CreateRevoluteJoint(bodyA=self.torsoBody,
                                                        bodyB=self.upperArm1Body,
                                                        anchor=(0, upperArm1Top),
                                                        lowerAngle=-.5 * b2_pi,  # -90 degrees
                                                        upperAngle=.5 * b2_pi,  # 90 degrees
                                                        enableLimit=True,
                                                        maxMotorTorque=maxMotorTorque,
                                                        enableMotor=True)

        lowerArm1Top = upperArm1Top - upperArm1Box[1] * 2
        lowerArm1Box = (.35, 1.25)
        self.lowerArm1Position = (0, lowerArm1Top - lowerArm1Box[1])
        self.lowerArm1Body = world.CreateDynamicBody(position=self.lowerArm1Position)
        lowerArm1 = self.lowerArm1Body.CreatePolygonFixture(box=lowerArm1Box, density=1, friction=0.3,
                                                       filter=b2Filter(groupIndex=-1))
        self.elbow1Joint = world.CreateRevoluteJoint(bodyA=self.upperArm1Body,
                                                     bodyB=self.lowerArm1Body,
                                                     anchor=(0, lowerArm1Top),
                                                     lowerAngle=0,  # 0 degrees
                                                     upperAngle=.5 * b2_pi,  # 90 degrees
                                                     enableLimit=True,
                                                     maxMotorTorque=maxMotorTorque,
                                                     enableMotor=True)

        upperArm2Top = torsoTop
        upperArm2Box = (.35, 1.25)
        self.upperArm2Position = (0, upperArm2Top - upperArm2Box[1])
        self.upperArm2Body = world.CreateDynamicBody(position=self.upperArm2Position)
        upperArm2 = self.upperArm2Body.CreatePolygonFixture(box=upperArm2Box, density=1, friction=0.3,
                                                       filter=b2Filter(groupIndex=-1))
        self.shoulder2Joint = world.CreateRevoluteJoint(bodyA=self.torsoBody,
                                                        bodyB=self.upperArm2Body,
                                                        anchor=(0, upperArm2Top),
                                                        lowerAngle=-.5 * b2_pi,  # -90 degrees
                                                        upperAngle=.5 * b2_pi,  # 90 degrees
                                                        enableLimit=True,
                                                        maxMotorTorque=maxMotorTorque,
                                                        enableMotor=True)

        lowerArm2Top = upperArm2Top - upperArm2Box[1] * 2
        lowerArm2Box = (.35, 1.25)
        self.lowerArm2Position = (0, lowerArm2Top - lowerArm2Box[1])
        self.lowerArm2Body = world.CreateDynamicBody(position=self.lowerArm2Position)
        lowerArm2 = self.lowerArm2Body.CreatePolygonFixture(box=lowerArm2Box, density=1, friction=0.3,
                                                       filter=b2Filter(groupIndex=-1))
        self.elbow2Joint = world.CreateRevoluteJoint(bodyA=self.upperArm2Body,
                                                     bodyB=self.lowerArm2Body,
                                                     anchor=(0, lowerArm2Top),
                                                     lowerAngle=0,  # 0 degrees
                                                     upperAngle=.5 * b2_pi,  # 90 degrees
                                                     enableLimit=True,
                                                     maxMotorTorque=maxMotorTorque,
                                                     enableMotor=True)

        upperLeg1Top = torsoTop - torsoBox[1] * 2
        upperLeg1Box = (.5, 1.5)
        self.upperLeg1Position = (0, upperLeg1Top - upperLeg1Box[1])
        self.upperLeg1Body = world.CreateDynamicBody(position=self.upperLeg1Position)
        upperLeg1 = self.upperLeg1Body.CreatePolygonFixture(box=upperLeg1Box, density=1, friction=0.3,
                                                       filter=b2Filter(groupIndex=-1))
        self.hip1Joint = world.CreateRevoluteJoint(bodyA=self.torsoBody,
                                                   bodyB=self.upperLeg1Body,
                                                   anchor=(0, upperLeg1Top),
                                                   lowerAngle=-.25 * b2_pi,  # 45 degres
                                                   upperAngle=.5 * b2_pi,  # 90 degrees
                                                   enableLimit=True,
                                                   maxMotorTorque=maxMotorTorque,
                                                   enableMotor=True)

        lowerLeg1Top = upperLeg1Top - upperLeg1Box[1] * 2
        lowerLeg1Box = (.5, 1.5)
        self.lowerLeg1Position = (0, lowerLeg1Top - lowerLeg1Box[1])
        self.lowerLeg1Body = world.CreateDynamicBody(position=self.lowerLeg1Position)
        lowerLeg1 = self.lowerLeg1Body.CreatePolygonFixture(box=lowerLeg1Box, density=1, friction=0.3,
                                                       filter=b2Filter(groupIndex=-1))
        self.knee1Joint = world.CreateRevoluteJoint(bodyA=self.upperLeg1Body,
                                                    bodyB=self.lowerLeg1Body,
                                                    anchor=(0, lowerLeg1Top),
                                                    lowerAngle=-.5 * b2_pi,  # 90 degrees
                                                    upperAngle=0 * b2_pi,  # 0 degrees
                                                    enableLimit=True,
                                                    maxMotorTorque=maxMotorTorque,
                                                    enableMotor=True)

        foot1Top = lowerLeg1Top - lowerLeg1Box[1] * 2
        foot1Box = (1, .25)
        self.foot1Position = (0 + lowerLeg1Box[0], foot1Top - foot1Box[1])
        self.foot1Body = world.CreateDynamicBody(position=self.foot1Position)
        foot1 = self.foot1Body.CreatePolygonFixture(box=foot1Box, density=1, friction=0.3, filter=b2Filter(groupIndex=-1))
        self.ankle1Joint = world.CreateRevoluteJoint(bodyA=self.lowerLeg1Body,
                                                     bodyB=self.foot1Body,
                                                     anchor=(0, foot1Top),
                                                     lowerAngle=-.25 * b2_pi,  # 45 degrees
                                                     upperAngle=.25 * b2_pi,  # 45 degrees
                                                     enableLimit=True,
                                                     maxMotorTorque=maxMotorTorque,
                                                     enableMotor=True)

        upperLeg2Top = torsoTop - torsoBox[1] * 2
        upperLeg2Box = (.5, 1.5)
        self.upperLeg2Position = (0, upperLeg2Top - upperLeg2Box[1])
        self.upperLeg2Body = world.CreateDynamicBody(position=self.upperLeg2Position)
        upperLeg2 = self.upperLeg2Body.CreatePolygonFixture(box=upperLeg2Box, density=1, friction=0.3,
                                                       filter=b2Filter(groupIndex=-1))
        self.hip2Joint = world.CreateRevoluteJoint(bodyA=self.torsoBody,
                                                   bodyB=self.upperLeg2Body,
                                                   anchor=(0, upperLeg2Top),
                                                   lowerAngle=-.25 * b2_pi,  # 45 degres
                                                   upperAngle=.5 * b2_pi,  # 90 degrees
                                                   enableLimit=True,
                                                   maxMotorTorque=maxMotorTorque,
                                                   enableMotor=True)

        lowerLeg2Top = upperLeg2Top - upperLeg2Box[1] * 2
        lowerLeg2Box = (.5, 1.5)
        self.lowerLeg2Position = (0, lowerLeg2Top - lowerLeg2Box[1])
        self.lowerLeg2Body = world.CreateDynamicBody(position=self.lowerLeg2Position)
        lowerLeg2 = self.lowerLeg2Body.CreatePolygonFixture(box=lowerLeg2Box, density=1, friction=0.3,
                                                       filter=b2Filter(groupIndex=-1))
        self.knee2Joint = world.CreateRevoluteJoint(bodyA=self.upperLeg2Body,
                                                    bodyB=self.lowerLeg2Body,
                                                    anchor=(0, lowerLeg2Top),
                                                    lowerAngle=-.5 * b2_pi,  # 90 degrees
                                                    upperAngle=0 * b2_pi,  # 0 degrees
                                                    enableLimit=True,
                                                    maxMotorTorque=maxMotorTorque,
                                                    enableMotor=True)

        foot2Top = lowerLeg2Top - lowerLeg2Box[1] * 2
        foot2Box = (1, .25)
        self.foot2Position = (0 + lowerLeg2Box[0], foot2Top - foot2Box[1])
        self.foot2Body = world.CreateDynamicBody(position=self.foot2Position)
        foot2 = self.foot2Body.CreatePolygonFixture(box=foot2Box, density=1, friction=0.3, filter=b2Filter(groupIndex=-1))
        self.ankle2Joint = world.CreateRevoluteJoint(bodyA=self.lowerLeg2Body,
                                                     bodyB=self.foot2Body,
                                                     anchor=(0, foot2Top),
                                                     lowerAngle=-.25 * b2_pi,  # 45 degrees
                                                     upperAngle=.25 * b2_pi,  # 45 degrees
                                                     enableLimit=True,
                                                     maxMotorTorque=maxMotorTorque,
                                                     enableMotor=True)

        # Move a legs and arms slightly so that they diverge on start
        self.upperLeg1Body.ApplyAngularImpulse(impulse=1, wake=True)
        self.upperLeg2Body.ApplyAngularImpulse(impulse=-1, wake=True)
        self.upperArm1Body.ApplyAngularImpulse(impulse=1, wake=True)
        self.upperArm2Body.ApplyAngularImpulse(impulse=-1, wake=True)

    def __addBodyPart(self, world, position, box, bodyIndex, connectedBody = None, jointIndex = -1, jointAngles = (0,0)):
        self.positionList.append(position)
        body = world.CreateDynamicBody(position=position)
        body.CreatePolygonFixture(box=box, density=1, friction=0.3, filter=b2Filter(groupIndex = -1))
        self.bodyList[bodyIndex] = body
        if(not (connectedBody is None)):
            joint = world.CreateRevoluteJoint(bodyA=connectedBody,
                                              bodyB=body,
                                              anchor=(position[0], position[1] + box[1]),
                                              lowerAngle = jointAngles[0],
                                              upperAngle = jointAngles[1],
                                              enableLimit = True,
                                              maxMotorTorque = 100.0,
                                              enableMotor = True)
            self.jointList[jointIndex] = joint

    def getJointAngles(self):
        return (self.neckJoint.angle,
                self.shoulder1Joint.angle,
                self.elbow1Joint.angle,
                self.shoulder2Joint.angle,
                self.elbow2Joint.angle,
                self.hip1Joint.angle,
                self.knee1Joint.angle,
                self.ankle1Joint.angle,
                self.hip2Joint.angle,
                self.knee2Joint.angle,
                self.ankle2Joint.angle)

    def setJointForces(self, forces):
        self.neckJoint.motorSpeed = forces[0]
        self.shoulder1Joint.motorSpeed = forces[1]
        self.elbow1Joint.motorSpeed = forces[2]
        self.shoulder2Joint.motorSpeed = forces[3]
        self.elbow2Joint.motorSpeed = forces[4]
        self.hip1Joint.motorSpeed = forces[5]
        self.knee1Joint.motorSpeed = forces[6]
        self.ankle1Joint.motorSpeed = forces[7]
        self.hip2Joint.motorSpeed = forces[8]
        self.knee2Joint.motorSpeed = forces[9]
        self.ankle2Joint.motorSpeed = forces[10]

    def getTorsoPosition(self):
        return self.torsoBody.position[0]

    def resetPosition(self):
        self.headBody.transform = [self.headPosition, 0]
        self.torsoBody.transform = [self.torsoPosition, 0]
        self.upperArm1Body.transform = [self.upperArm1Position, 0]
        self.lowerArm1Body.transform = [self.lowerArm1Position, 0]
        self.upperArm2Body.transform = [self.upperArm2Position, 0]
        self.lowerArm2Body.transform = [self.lowerArm2Position, 0]
        self.upperLeg1Body.transform = [self.upperLeg1Position, 0]
        self.lowerLeg1Body.transform = [self.lowerLeg1Position, 0]
        self.foot1Body.transform = [self.foot1Position, 0]
        self.upperLeg2Body.transform = [self.upperLeg2Position, 0]
        self.lowerLeg2Body.transform = [self.lowerLeg2Position, 0]
        self.foot2Body.transform = [self.foot2Position, 0]
