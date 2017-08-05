from simulator import Simulator
import framework
import simulatorSettings

useGraphics = False

if(useGraphics):
    framework.main(Simulator)
else:
    simulator = Simulator(False)
    while(True):
        simulator.Step(simulatorSettings.fwSettings)