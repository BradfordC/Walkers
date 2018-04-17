from evolution import selection

class Performance:
    def __init__(self):
        #How much an agent moved over the course of the run
        self.displacement = (0,0)
        #History of the agent during its generation, used for similarity testing
        self.history = []
        #How unique an agent is compared to the rest of a population
        self.novelty = None
        #How well an agent is doing to be chosen for reproduction
        self.score = None

    def setDisplacement(self, startPosition, endPosition):
        xDif = endPosition[0] - startPosition[0]
        yDif = endPosition[1] - startPosition[1]
        self.displacement = (xDif, yDif)

    def getFitness(self):
        #Currently fitness is just X displacement
        return self.displacement[0]

    #Compare the two agents' histories to see how different the two are
    def getHistoryDistance(self, otherPerformance):
        if(len(self.history) != len (otherPerformance.history)):
            print("Error: Histories are not the same size.")
            return None

        totalSquaredDifference = 0

        #For each state, check the difference between all values
        for stateIndex in range(len(self.history)):
            myState = self.history[stateIndex]
            otherState = otherPerformance.history[stateIndex]

            if(len(myState) != len(otherState)):
                print("Error: States are not the same size.")
                return None

            for i in range(len(myState)):
                totalSquaredDifference += (myState[i] - otherState[i]) ** 2

        distance = totalSquaredDifference ** 0.5
        return distance

    #Calculate the novelty of an agent based on the performances of the rest of a population
    def setNovelty(self, performanceList):
        totalDistance = 0
        for otherPerformance in performanceList:
            #Don't check the distance against itself
            if(otherPerformance is not self):
                totalDistance += self.getHistoryDistance(otherPerformance)
        #Don't count itself when finding average
        averageDistance = totalDistance / (len(performanceList) - 1)
        self.noveltyScore = averageDistance

    def getNovelty(self):
        return self.noveltyScore

    def getScore(self, selectionCriteria):
        if(selectionCriteria == selection.OBJECTIVE or selectionCriteria == selection.SPECIATION):
            self.score = self.getFitness()
        elif(selectionCriteria == selection.NOVELTY):
            self.score = self.getNovelty()
        elif(selectionCriteria == selection.COMBINED):
            self.score = self.getFitness() + self.getNovelty()
        return self.score
