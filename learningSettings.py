from evolution import selection

class learningSettings:
    useGraphics = True
    useSimpleWalkers = False

    loadPopulation = False
    populationFile = "D:/Chris/Dropbox/Dropbox/School/Research/Walkers/results/populations/Test--2018-04-19--14-16-12.pop"

    selectionCriteria = selection.OBJECTIVE
    fileName = 'Test'

    secondsPerRun = 5
    walkerCount = 100
    groupSize = 50
    numberOfGenerations = 100
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