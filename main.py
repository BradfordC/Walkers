from simulator import Simulator
import framework
import physicsSettings
from learningSettings import learningSettings

if(learningSettings.useGraphics):
    framework.main(Simulator)
else:
    simulator = Simulator(False)
    while(True):
        simulator.Step(physicsSettings.fwSettings)