import pygame
from myLibrary import *
from QLearning import QTable

import numpy as np
import json
import sys
from matplotlib import pyplot as plt


class CmdLine:
    def __init__(self, qTable: QTable, avgSpeedList: list[float]) -> None:
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

        self.avgSpeedList = avgSpeedList

        self.gathering = False
        self.nbSample = 1000
        self.jamitonSamples = np.zeros(self.nbSample)
        self.sampleId = 0
        self.plotPath = None

    def processCmd(self):
        command = self.text[1:]
        tokens = command.split(" ")

        if tokens[0] == "echo":
            print(" ".join(tokens[1:]))

        elif tokens[0] == "qTable":
            print(self.qTable.qTable)

        elif tokens[0] == "save":
            self.saveCmd(tokens)

        elif tokens[0] == "load":
            self.loadCmd(tokens)

        elif tokens[0] == "q":
            self.debugDict["isRunning"]
            sys.exit()

        elif tokens[0] == "set":
            self.setCmd(tokens)

        elif tokens[0] == "perturb":
            self.perturbCmd()

        elif tokens[0] == "plot":
            self.plotCmd()

        elif tokens[0] == "gather":
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
            with open("qTable0.json", "w") as saveFile:
                qTableList = self.qTable.qTable.tolist()
                json.dump(qTableList, saveFile)
            print("Saved QTable to {qTable0.json}")
            return

        fileName = tokens[1]
        with open(f"qTable{fileName}.json", "w") as saveFile:
            qTableList = self.qTable.qTable.tolist()
            json.dump(qTableList, saveFile)
        print(f"Saved QTable to qTable{fileName}.json")

    def loadCmd(self, tokens):
        if len(tokens) == 1:
            with open("qTable0.json", "r") as saveFile:
                qTableList = json.load(saveFile)
                self.qTable.qTable = np.array(qTableList)
            print("Loaded QTable from qTable0.json")
            return

        fileName = tokens[1]
        with open(f"qTable{fileName}.json", "r") as saveFile:
            qTableList = json.load(saveFile)
            self.qTable.qTable = np.array(qTableList)
        print(f"Loaded QTable from qTable{fileName}.json")

    def setCmd(self, tokens):
        if len(tokens) < 3:
            print("Missing arguments for set command")
            return

        if tokens[1] == "epsilon":
            self.qTable.epsilon = float(tokens[2])
            return

    def perturbCmd(self):
        newState = not self.carList[0].perturbing
        self.carList[0].perturbing = newState
        self.debugDict["perturbing"] = newState

    def plotCmd(self):
        yValues = np.array(self.avgSpeedList)
        xValues = np.arange(len(self.avgSpeedList))

        plt.plot(xValues, yValues)
        print("Plotting avg speed")
        plt.savefig("./example.pdf")

    def startGatheringCmd(self, tokens: list[str]):
        """
        set
            "Perturb Interval": 950,
            "Perturb Duration": 50,
        create a numpy array of 10000
        run the sim for 10000 iterations
        """
        if len(tokens) > 2:
            print(f"Too many args were given ({len(tokens)}), expected (1)")
            return
        if len(tokens) == 1 and self.plotPath == None:
            print("C'est quoi le nom zebi ?")
            return

        if not self.gathering:
            self.plotPath = f"./{tokens[1]}.pdf"
            self.gathering = True
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

        jamitonValue = computeJamitonsInt(self.carList)
        print(f"jamitonValue : {jamitonValue}")
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
