from simulator import Simulator
import framework
import physicsSettings
from learningSettings import learningSettings
import cProfile

def test():
    simulator = Simulator(False)
    while(True):
        simulator.Step(physicsSettings.fwSettings)

if(learningSettings.useGraphics):
    framework.main(Simulator)
else:
    cProfile.runctx('test()', globals(), locals(), 'profileResults1.pstats')