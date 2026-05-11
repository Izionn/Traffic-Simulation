import pygame
from myLibrary import *
from QLearning import QTable

import numpy as np
import json
import sys
from matplotlib import pyplot as plt


class CmdLine:
    def __init__(
        self,
        qTable: QTable,
    ) -> None:
        self.display = pygame.display.get_surface()
        assert type(self.display) == pygame.Surface
        self.displaySize = self.display.get_size()

        self.width = self.displaySize[0]
        self.heigth = 28
        self.posX = 0
        self.posY = self.displaySize[1] - self.heigth

        self.bgColor = pygame.Color("#1a1a1a")
        self.surface = pygame.Surface((self.width, self.heigth))
        self.surface.fill(self.bgColor)

        self.opened = False

        self.text = ":"
        self.font = pygame.font.Font(r"./FiraCodeNerdFontMono-Light.ttf", 20)
        self.textColor = pygame.Color("#ffffff")

        self.qTable = qTable
        self.carList = self.qTable.carList
        self.debugDict = self.qTable.debugDict
        self.valueDict = self.qTable.valueDict

        self.gathering = False
        self.nbSample = 5000
        self.jamitonSamples = np.zeros(self.nbSample)
        self.sampleId = 0
        self.plotPath = None

    def processCmd(self):
        command = self.text[1:]
        tokens = command.split(" ")

        if tokens[0] == "save":
            self.saveCmd(tokens)

        elif tokens[0] == "load":
            self.loadCmd(tokens)

        elif tokens[0] == "q" or tokens[0] == "quit":
            self.debugDict["isRunning"]
            sys.exit()

        elif tokens[0] == "set":
            self.setCmd(tokens)

        elif tokens[0] == "perturb":
            self.perturbCmd()

        elif tokens[0] == "gather" or tokens[0] == "g":
            self.startGatheringCmd(tokens)

        else:
            print(f"Unknown command : {tokens[0]}")

        self.close()

    def draw(self):
        if not self.opened:
            return

        self.surface.fill(self.bgColor)

        textSurf = self.font.render(self.text, False, self.textColor)
        self.surface.blit(textSurf, (0, 0))
        assert type(self.display) == pygame.Surface
        self.display.blit(self.surface, (self.posX, self.posY))

    def open(self):
        self.opened = True
        self.text = ":"

    def close(self):
        self.opened = False
        self.text = ":"

    def saveCmd(self, tokens):
        if len(tokens) == 1:
            print("Expected a name for save command")
            return

        savePath = f"./data/qTable{tokens[1]}.json"
        with open(savePath, "w") as saveFile:
            qTableList = self.qTable.qTable.tolist()
            json.dump(qTableList, saveFile)
        print(f"Saved QTable to {savePath}")

    def loadCmd(self, tokens):

        if len(tokens) == 1:
            print("Expected a name for load command")
            return

        savePath = f"./data/qTable{tokens[1]}.json"
        with open(savePath, "r") as saveFile:
            qTableList = json.load(saveFile)
            qTableArray = np.array(qTableList)
            self.qTable.qTable = qTableArray
        print(f"Loaded QTable from {savePath}")

    def setCmd(self, tokens):
        if len(tokens) < 3:
            print("Missing arguments for set command")
            return

        if tokens[1] == "epsilon" or tokens[1] == "eps":
            self.qTable.epsilon = float(tokens[2])
            return

    def perturbCmd(self):
        newState = not self.carList[0].perturbing
        self.carList[0].perturbing = newState
        self.debugDict["perturbing"] = newState

    def startGatheringCmd(self, tokens: list[str]):

        if len(tokens) > 2:
            print(f"Too many args were given ({len(tokens)}), expected (1)")
            return
        if len(tokens) == 1 and self.plotPath == None:
            print("Expected a name for plot")
            return

        self.valueDict["Perturb Duration"] = 100

        if not self.gathering:
            self.plotPath = f"./data/{tokens[1]}.pdf"
            self.gathering = True

            self.debugDict["perturbing"] = True

            firstCar = self.carList[0]
            firstCar.stopped = True
            firstCar.perturbing = True
            firstCar.perturbingOnce = True
            firstCar.perturbTimeLeft = firstCar.perturbDuration

            print("Started gathering data")

        else:
            print("Already gathering data")
            print(
                f"Currently at {self.sampleId} / {self.nbSample} samples. ({round(self.sampleId / self.nbSample * 100)}%) "
            )
        print(f"Storing plot at {self.plotPath}")

    def gatherData(self):

        if not self.gathering:
            return

        jamitonValue = computeJamitonValue(self.carList)
        self.jamitonSamples[self.sampleId] = jamitonValue
        self.sampleId += 1

        if self.sampleId == self.nbSample:

            xPoints = np.arange(self.nbSample)

            plt.xlabel("Iteration")
            plt.ylabel("Jamiton Value")

            plt.plot(xPoints, self.jamitonSamples)
            plt.savefig(self.plotPath)
            plt.cla()

            print("Data gathering done")
            print(f"Stored at {self.plotPath}")

            self.gathering = False
            self.plotPath = None
            self.sampleId = 0
            self.jamitonSamples.fill(0)

        elif self.sampleId % 100 == 0:
            xPoints = np.arange(self.nbSample)

            plt.xlabel("Iteration")
            plt.ylabel("Jamiton Value")

            plt.plot(xPoints, self.jamitonSamples)
            plt.savefig(self.plotPath)
            plt.cla()
