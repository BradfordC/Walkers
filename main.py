from simulator import Simulator
import framework
import settings

useGraphics = True

if(useGraphics):
    framework.main(Simulator)
else:
    simulator = Simulator(False)
    while(True):
        simulator.Step(settings.fwSettings)