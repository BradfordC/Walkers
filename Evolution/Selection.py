from Evolution import Population, Agent
import random

#Returns a parent based on tournament selection
def TournamentSelect(population, tournamentSize):
    tournamentCandidates = random.sample(range(len(population.agentList), tournamentSize))

    #Find the best candidate in tournament
    largestFitness = -999999
    largestIndex = -1
    for candidate in tournamentCandidates:
        candidateFitness = population.agentList[candidate].fitness
        if(candidateFitness > largestFitness):
            largestFitness = candidateFitness
            largestIndex = candidate

    return largestIndex