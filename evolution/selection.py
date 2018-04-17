import random

OBJECTIVE = 0
NOVELTY = 1
COMBINED = 2
SPECIATION = 3

#Returns a parent based on tournament selection
def TournamentSelect(agentList, tournamentSize, selectionCriteria):
    tournamentCandidates = random.sample(range(len(agentList)), tournamentSize)

    #Find the best candidate in tournament
    largestScore = -999999
    largestIndex = -1
    for candidate in tournamentCandidates:
        candidateScore = agentList[candidate].performance.getScore(selectionCriteria)

        if(candidateScore > largestScore):
            largestScore = candidateScore
            largestIndex = candidate

    return largestIndex