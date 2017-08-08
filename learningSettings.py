from evolution import selection

class learningSettings:
    useGraphics = False

    selectionCriteria = selection.NOVELTY
    fileName = 'Test'

    secondsPerRun = 5
    walkerCount = 50
    numberOfGenerations = 100
    numberOfExperiments = 1

    #Speciation
    initialEnergy = 5
    foodCount = 10
    foodUses = 5

    choosinessLimit = 10