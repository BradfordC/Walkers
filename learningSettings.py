from evolution import selection

class learningSettings:
    useGraphics = False
    useSimpleWalkers = False

    loadPopulation = False
    populationFile = "D:/Chris/Dropbox/Dropbox/School/Research/Walkers/results/populations/Novelty--2018-04-25--18-30-45.pop"

    selectionCriteria = selection.NOVELTY
    fileName = 'Novelty'

    secondsPerRun = 7
    walkerCount = 1000
    groupSize = 50
    numberOfGenerations = 200
    numberOfExperiments = 3

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