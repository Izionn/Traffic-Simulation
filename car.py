import pygame
import numpy as np
from myLibrary import *

pygame.init()


class Car:
    def __init__(self, valuesDict, roadRadius, carId, carAngleList, carList) -> None:
        self.display = pygame.display.get_surface()
        self.displaySize = self.display.get_size()
        self.roadCenter = self.displaySize[1] // 2, self.displaySize[1] // 2

        self.valuesDict = valuesDict

        self.radius = 5
        self.redValue = 0
        self.greenValue = 0
        self.color = pygame.Color("Red")

        self.roadRadius = roadRadius

        self.carAngleList = carAngleList
        self.nbCars = len(self.carAngleList)
        self.carId = carId
        self.nextCarId = (self.carId + 1) % self.nbCars
        self.carList = carList
        self.angle = carAngleList[carId]
        self.posX = self.roadRadius * np.cos(degToRad(self.angle)) + self.roadCenter[0]
        self.posY = self.roadRadius * np.sin(degToRad(self.angle)) + self.roadCenter[1]

        self.speed = 0
        self.currentMaxSpeed = 0
        self.stopped = False

        # car constants
        self.minDistance = self.valuesDict["Min Distance"]
        self.acceleration = self.valuesDict["Acceleration"]
        self.maxSpeed = self.valuesDict["Max Speed"]
        self.minSpeed = 0
        self.reactionTime = self.valuesDict["Reaction Time"]

    def setSpeed(self, speed):
        self.speed = speed

    def getSpeed(self):
        return self.speed

    def update(self):

        self.greenValue = round(self.speed / (self.maxSpeed - self.minSpeed) * 255)
        self.redValue = round(
            (self.maxSpeed - self.speed) / (self.maxSpeed - self.minSpeed) * 255
        )
        self.redValue = max([0, self.redValue])
        self.redValue = min([255, self.redValue])

        self.greenValue = max([0, self.greenValue])
        self.greenValue = min([255, self.greenValue])

        self.color = pygame.Color(self.redValue, self.greenValue, 0)
        self.move()

    def updatesIds(self):
        self.nbCars = len(self.carAngleList)
        self.nextCarId = (self.carId + 1) % self.nbCars

    def updateValues(self):
        self.minDistance = self.valuesDict["Min Distance"]
        self.acceleration = self.valuesDict["Acceleration"]
        self.maxSpeed = self.valuesDict["Max Speed"]
        self.reactionTime = self.valuesDict["Reaction Time"]
        self.nbCars = len(self.carAngleList)

    def move(self):

        deltaAngle = (self.carAngleList[self.nextCarId] - self.angle) % 360
        distToNextCar = deltaAngle * self.roadRadius

        if self.stopped:
            self.currentMaxSpeed = 0

        elif distToNextCar <= self.minDistance:
            self.currentMaxSpeed = 0
        elif distToNextCar > self.reactionTime * self.maxSpeed:
            self.currentMaxSpeed = self.maxSpeed
        else:
            self.currentMaxSpeed = distToNextCar / self.reactionTime

        if self.speed < self.currentMaxSpeed:
            self.speed = min(self.speed + self.acceleration, self.currentMaxSpeed)
        if self.speed > self.currentMaxSpeed:
            self.speed = max(self.speed - self.acceleration, self.currentMaxSpeed)

        if self.stopped:
            self.speed = max(self.speed - self.acceleration, 0)

        radialSpeed = self.speed / self.roadRadius

        self.angle = (radialSpeed + self.angle) % 360
        self.carAngleList[self.carId] = self.angle

        self.posX = self.roadRadius * np.cos(degToRad(self.angle)) + self.roadCenter[0]
        self.posY = self.roadRadius * np.sin(degToRad(self.angle)) + self.roadCenter[1]

    def draw(self):
        pygame.draw.circle(
            self.display,
            self.color,
            (self.posX, self.posY),
            self.radius,
        )
