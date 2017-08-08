from evolution import selection

class learningSettings:
    useGraphics = False

    selectionCriteria = selection.NOVELTY
    fileName = 'Test'

    secondsPerRun = 10
    walkerCount = 100
    numberOfGenerations = 100
    numberOfExperiments = 1

    #Speciation
    initialEnergy = 5
    foodCount = 10
    foodUses = 5

    choosinessLimit = 6