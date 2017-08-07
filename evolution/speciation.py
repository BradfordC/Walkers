import walker

def generateFood(walker, arraySize):
    food = []
    for i in range(arraySize):
        food.append(walker.getRandomJointAngles())
    return food