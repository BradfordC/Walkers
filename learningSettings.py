from evolution import selection

class learningSettings:
    useGraphics = False
    useSimpleWalkers = False

    selectionCriteria = selection.SPECIATION
    fileName = 'Test'

    secondsPerRun = 5
    walkerCount = 100
    numberOfGenerations = 100
    numberOfExperiments = 1

    #Speciation
    maxEnergy = 5
    initialEnergy = 1

    foodCount = 1000
    foodUses = 5
    foodEnergy = 2

    runsBetweenBreeding = 1

    choosinessLimit = secondsPerRun * .5