from simulator import Simulator
import framework
import settings

useGraphics = False

if(useGraphics):
    framework.main(Simulator)
else:
    simulator = Simulator(False)
    while(True):
        simulator.Step(settings.fwSettings)