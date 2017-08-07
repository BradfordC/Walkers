import random

OBJECTIVE = 0
NOVELTY = 1
COMBINED = 2

#Returns a parent based on tournament selection
def TournamentSelect(agentList, tournamentSize, selectionCriteria):
    tournamentCandidates = random.sample(range(len(agentList)), tournamentSize)

    #Find the best candidate in tournament
    largestFitness = -999999
    largestIndex = -1
    for candidate in tournamentCandidates:
        candidateFitness = 0
        if(selectionCriteria == OBJECTIVE):
            candidateFitness = agentList[candidate].fitness
        elif(selectionCriteria == NOVELTY):
            candidateFitness = agentList[candidate].novelty
        elif(selectionCriteria == COMBINED):
            candidateFitness = agentList[candidate].fitness + agentList[candidate].novelty

        if(candidateFitness > largestFitness):
            largestFitness = candidateFitness
            largestIndex = candidate

    return largestIndex