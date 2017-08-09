from evolution import selection

class learningSettings:
    useGraphics = True
    useSimpleWalkers = False

    selectionCriteria = selection.SPECIATION
    fileName = 'Test'

    secondsPerRun = 10
    walkerCount = 20
    numberOfGenerations = 100
    numberOfExperiments = 1

    #Speciation
    initialEnergy = 3
    foodCount = 10
    foodUses = 5
    foodEnergy = 3

    choosinessLimit = secondsPerRun * .5