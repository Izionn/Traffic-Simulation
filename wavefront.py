import pygame
from math import cos, sin
from car import Car
from myLibrary import *


class Wavefront:
    def __init__(self, carList: list[Car], valueDict, roadRadius: int) -> None:
        self.display = pygame.display.get_surface()
        self.displaySize = self.display.get_size()
        self.roadCenter = self.displaySize[1] // 2, self.displaySize[1] // 2

        self.roadRadius = roadRadius

        self.carList = carList
        self.valueDict = valueDict

        self.startFrontAngle = 0
        self.endFrontAngle = 10

        self.frontsHidden = False

    def update(self):
        self.updateFrontsAngle()
        if not self.frontsHidden:
            self.drawFronts()

    def updateFrontsAngle(self):
        self.updateExtremaSpeed()
        if self.minSpeedValue == self.maxSpeedValue:
            self.frontsHidden = True
            return

        self.frontsHidden = False
        self.startFrontAngle = self.carList[self.minSpeedId].angle
        self.endFrontAngle = self.carList[self.maxSpeedId].angle

    def drawFronts(self):

        frontsOffset = 33

        startFrontX = (self.roadRadius + frontsOffset) * cos(
            degToRad(self.startFrontAngle)
        ) + self.roadCenter[0]
        startFrontY = (self.roadRadius + frontsOffset) * sin(
            degToRad(self.startFrontAngle)
        ) + self.roadCenter[1]

        endFrontX = (self.roadRadius + frontsOffset) * cos(
            degToRad(self.endFrontAngle)
        ) + self.roadCenter[0]
        endFrontY = (self.roadRadius + frontsOffset) * sin(
            degToRad(self.endFrontAngle)
        ) + self.roadCenter[1]

        pygame.draw.circle(
            self.display, pygame.Color("#38a0ff"), (startFrontX, startFrontY), 5
        )
        pygame.draw.circle(
            self.display, pygame.Color("#14edff"), (endFrontX, endFrontY), 5
        )

    def updateExtremaSpeed(self):
        nbCar = len(self.carList)

        self.maxSpeedValue = self.carList[0].speed
        self.maxSpeedId = 0

        self.minSpeedValue = self.carList[0].speed
        self.minSpeedId = 0

        for i in range(nbCar):
            currentCar = self.carList[i]
            currentSpeed = currentCar.speed

            if currentSpeed > self.maxSpeedValue:
                self.maxSpeedValue = currentSpeed
                self.maxSpeedId = i

            if currentSpeed < self.minSpeedValue:
                self.minSpeedValue = currentSpeed
                self.minSpeedId = i
