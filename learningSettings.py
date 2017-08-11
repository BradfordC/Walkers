from evolution import selection

class learningSettings:
    useGraphics = False
    useSimpleWalkers = False

    selectionCriteria = selection.SPECIATION
    fileName = 'Speciation'

    secondsPerRun = 7
    walkerCount = 100
    numberOfGenerations = 100
    numberOfExperiments = 2

    #Speciation
    staticFood = False

    maxEnergy = 5
    initialEnergy = 1

    foodCount = 50
    foodUses = 3
    foodEnergy = 1

    runsBetweenBreeding = 1

    choosinessLimitFood = secondsPerRun * .8
    choosinessLimitMate = secondsPerRun * .5