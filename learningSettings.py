from evolution import selection

class learningSettings:
    useGraphics = False

    selectionCriteria = selection.COMBINED
    fileName = 'Combined2x'

    secondsPerRun = 100
    walkerCount = 500
    numberOfGenerations = 200
    numberOfExperiments = 1

    #Speciation
    initialEnergy = 5
    foodCount = 10
    foodUses = 5