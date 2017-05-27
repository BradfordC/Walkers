from Networks import Layer
from Networks import OutputLayer
import numpy as np

class Network:
    def __init__(self, inputSize, outputSize, hiddenLayerSizes, useDropout=False, activationFunction="Sigmoid"):
        self.Layers = []

        layerSizes = [inputSize]
        layerSizes.extend(hiddenLayerSizes)
        layerSizes.append(outputSize)

        for i in range(0, len(layerSizes) - 1):
            newLayer = Layer.Layer(layerSizes[i], layerSizes[i+1], .5 if useDropout else 0, activationFunction)
            newLayer.RandomizeWeights()
            self.Layers.append(newLayer)
        self.Layers[0].Mode = "Linear"
        self.Layers[0].DropoutRate = .2 if useDropout else 0

        self.OutputLayer = OutputLayer.OutputLayer(outputSize)

    @classmethod
    def fromNetwork(cls, otherNetwork):
        layerSizes = otherNetwork.GetLayerSizes()
        return Network(layerSizes[0], layerSizes[-1], layerSizes[1:-1])

    def Feedforwad(self, input):
        if(type(input) is list):
            input = np.array(input)
        nextLayerInput = input.copy()
        for layer in self.Layers:
            nextLayerInput = layer.Feedforward(nextLayerInput)
        self.OutputLayer.Activate(nextLayerInput)
        return self.OutputLayer.GetOutput()

    def GetError(self, expected):
        return self.OutputLayer.GetError(expected)

    def Backprop(self, expected, learningRate):
        nextLayerDeltas = self.OutputLayer.GetDeltas(expected)
        for layer in reversed(self.Layers):
            gradient = np.dot(nextLayerDeltas.reshape(nextLayerDeltas.size, 1), layer.Activations.reshape(1,layer.Activations.size))
            layer.Weights = np.add(layer.Weights, np.multiply(gradient,learningRate))
            nextLayerDeltas = layer.MakeDeltas(nextLayerDeltas)

    def GetLayerSizes(self):
        sizes = []
        for Layer in self.Layers:
            sizes.append(Layer.Size)
        sizes.append(self.OutputLayer.Size)
        return sizes