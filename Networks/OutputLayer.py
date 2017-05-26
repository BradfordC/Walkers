import numpy as np
import math
from Networks import Functions

class OutputLayer:
    def __init__(self, size, errorFunction="MSE"):
        self.Size = size
        self.ErrorFunction = errorFunction

        self.Values = np.zeros(self.Size)
        self.Activations = np.zeros(self.Size)

    def Activate(self, values):
        if self.Values.size != values.size:
            print("Input size didn't match: {} vs {}".format(self.Values.size, values.size))
            return

        self.Values = values.copy()

        #Sigmoid
        for i in range(0, self.Values.size):
            #Hack
            #Using max to prevent overflow error
            value = max(self.Values[i], -700)
            self.Activations[i] = Functions.Sigmoid(value)

    def GetOutput(self):
        return self.Activations.copy()

    def GetError(self, expected):
        if self.Values.size != expected.size:
            return

        if self.ErrorFunction == "MSE":
            errorSum = 0
            for i in range(0, self.Activations.size):
                error = math.pow(self.Activations[i] - expected[i], 2)
                errorSum += error
            mse = errorSum / self.Activations.size
            return mse

    def GetDeltas(self, expected):
        deltas = np.zeros(self.Size)
        for i in range(0, self.Size):
            deltas[i] = expected[i] - self.Activations[i]
        return deltas