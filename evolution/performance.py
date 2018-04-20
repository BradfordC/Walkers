from evolution import selection

class Performance:
    def __init__(self):
        #History of the agent's position over the course of a run
        self.history = []
        #History of the agent's joints during its generation, used for similarity testing
        self.jointHistory = []
        #How unique an agent is compared to the rest of a population
        self.novelty = None
        #How well an agent is doing to be chosen for reproduction
        self.score = None

    def addToHistory(self, position):
        self.history.append(position)

    def addToJointHistory(self, jointAngles):
        self.jointHistory.append(jointAngles)

    def getDistanceTravelled(self):
        #Return the X value of the last position
        return self.history[-1][0]

    def getFitness(self):
        sum = 0
        for position in self.history:
            sum += position[0] + (position[1] * .5)
        return sum

    #Compare the two agents' joint histories to see how different the two are
    def getJointHistoryDistance(self, otherPerformance):
        if(len(self.jointHistory) != len (otherPerformance.jointHistory)):
            print("Error: Histories are not the same size.")
            return None

        totalSquaredDifference = 0

        #For each state, check the difference between all values
        for stateIndex in range(len(self.jointHistory)):
            myState = self.jointHistory[stateIndex]
            otherState = otherPerformance.jointHistory[stateIndex]

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
                totalDistance += self.getJointHistoryDistance(otherPerformance)
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
