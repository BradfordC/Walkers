import datetime

class fileHandler:
    resultsDirectory = 'results/'

    def __init__(self, fileBaseName):
        currentTime = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")

        self.fileName = fileHandler.resultsDirectory + fileBaseName + '--' + currentTime + '.txt'

    def write(self, line):
        with open(self.fileName, 'a') as file:
            file.write(line)