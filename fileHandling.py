import datetime
import os

class fileHandler:
    resultsDirectory = 'results/'
    popDirectory = resultsDirectory + 'populations/'

    def __init__(self, fileBaseName):
        currentTime = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")

        self.fileName = fileHandler.resultsDirectory + fileBaseName + '--' + currentTime + '.txt'
        self.popSaveName = fileHandler.popDirectory + fileBaseName + '--' + currentTime + '.pop'

        self.makeDirs()

    def write(self, line):
        with open(self.fileName, 'a') as file:
            file.write(line)

    def makeDirs(self):
        if(not os.path.exists(fileHandler.resultsDirectory)):
            os.makedirs(fileHandler.resultsDirectory)

        if(not os.path.exists(fileHandler.popDirectory)):
            os.makedirs(fileHandler.popDirectory)