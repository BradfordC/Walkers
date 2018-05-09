from evolution import selection

class learningSettings:
    useGraphics = False
    useSimpleWalkers = False

    loadPopulation = False
    populationFile = "D:/Chris/Dropbox/Dropbox/School/Research/Walkers/results/populations/Novelty--2018-04-25--18-30-45.pop"

    selectionCriteria = selection.SPECIATION
    fileName = 'Test'

    secondsPerRun = 7
    walkerCount = 500
    groupSize = 50
    numberOfGenerations = 200
    numberOfExperiments = 3

    tournamentSize = 4

    #Speciation
    staticFood = False

    maxEnergy = 5
    initialEnergy = 2

    foodCount = 500
    foodUses = 3
    foodEnergy = 2

    runsBetweenBreeding = 1

    choosinessLimitFood = secondsPerRun * 1
    choosinessLimitMate = secondsPerRun * 1