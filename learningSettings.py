from evolution import selection

class learningSettings:
    useGraphics = True
    useSimpleWalkers = False

    selectionCriteria = selection.OBJECTIVE
    fileName = 'Test'

    secondsPerRun = 7
    walkerCount = 5
    numberOfGenerations = 100
    numberOfExperiments = 1

    #Speciation
    staticFood = False

    maxEnergy = 5
    initialEnergy = 1

    foodCount = 100
    foodUses = 3
    foodEnergy = 1

    runsBetweenBreeding = 1

    choosinessLimitFood = secondsPerRun * .8
    choosinessLimitMate = secondsPerRun * .5