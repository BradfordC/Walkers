from evolution import selection

class learningSettings:
    useGraphics = True
    useSimpleWalkers = False

    selectionCriteria = selection.NOVELTY
    fileName = 'Test'

    secondsPerRun = 5
    walkerCount = 100
    groupSize = 25
    numberOfGenerations = 10
    numberOfExperiments = 1

    tournamentSize = 4

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