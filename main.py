from simulator import Simulator
import framework
import simulatorSettings
from learningSettings import learningSettings

if(learningSettings.useGraphics):
    framework.main(Simulator)
else:
    simulator = Simulator(False)
    while(True):
        simulator.Step(simulatorSettings.fwSettings)