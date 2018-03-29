from evolution import selection

class learningSettings:
    useGraphics = False
    useSimpleWalkers = False

    selectionCriteria = selection.OBJECTIVE
    fileName = 'Test'

    secondsPerRun = 3
    walkerCount = 10
    groupSize = walkerCount
    numberOfGenerations = 10
    numberOfExperiments = 1

    tournamentSize = 3

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