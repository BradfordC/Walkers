from enum import Enum
import random

class Crossover:
    class Types(Enum):
        SINGLE_POINT = 0
        DOUBLE_POINT = 1
        UNIFORM = 2

    @staticmethod
    def getRandomType():
        return random.choice(list(Crossover.Types))

    @staticmethod
    def crossRandomType(firstLayer, secondLayer, childLayer):
        crossoverType = Crossover.getRandomType()
        if(crossoverType == Crossover.Types.SINGLE_POINT):
            Crossover.crossSinglePoint(firstLayer, secondLayer, childLayer)
        elif(crossoverType == Crossover.Types.DOUBLE_POINT):
            Crossover.crossDoublePoint(firstLayer, secondLayer, childLayer)
        elif(crossoverType == Crossover.Types.UNIFORM):
            Crossover.crossUniform(firstLayer, secondLayer, childLayer)
        else:
            print("ERROR: Trying to use an unimplemented type of crossover.")

    @staticmethod
    def crossSinglePoint(firstLayer, secondLayer, childLayer):
            #For each row of weights, pick a random point
            #The weights before that point come from the first parent, the rest come from the second
            for row in range(len(firstLayer.Weights)):
                firstLayerRow = firstLayer.Weights[row]
                secondLayerRow = secondLayer.Weights[row]
                childLayerRow = childLayer.Weights[row]

                crossoverPoint = random.randint(1,len(firstLayerRow) - 1) #Randint is inclusive of both numbers
                for column in range(len(firstLayerRow)):
                    if(column < crossoverPoint):
                        childLayerRow[column] = firstLayerRow[column]
                    else:
                        childLayerRow[column] = secondLayerRow[column]

    @staticmethod
    def crossDoublePoint(firstLayer, secondLayer, childLayer):
            #For each row of weights, pick two random points
            #The weights between the two points come from the second parent, the rest come from the first parent
            for row in range(len(firstLayer.Weights)):
                firstLayerRow = firstLayer.Weights[row]
                secondLayerRow = secondLayer.Weights[row]
                childLayerRow = childLayer.Weights[row]

                firstCrossoverPoint = random.randint(1, len(firstLayerRow) - 2) #Randint is inclusive of both numbers
                secondCrossoverPoint = random.randint(firstCrossoverPoint + 1, len(firstLayerRow) - 1)
                for column in range(len(firstLayerRow)):
                    if(column < firstCrossoverPoint or column >= secondCrossoverPoint):
                        childLayerRow[column] = firstLayerRow[column]
                    else:
                        childLayerRow[column] = secondLayerRow[column]

    @staticmethod
    def crossUniform(firstLayer, secondLayer, childLayer):
            #For each weight, choose randomly between using the first and the second parent's weight
            for row in range(len(firstLayer.Weights)):
                firstLayerRow = firstLayer.Weights[row]
                secondLayerRow = secondLayer.Weights[row]
                childLayerRow = childLayer.Weights[row]

                for column in range(len(firstLayerRow)):
                    if(random.random() < .5):
                        childLayerRow[column] = firstLayerRow[column]
                    else:
                        childLayerRow[column] = secondLayerRow[column]