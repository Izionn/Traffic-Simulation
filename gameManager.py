import pygame
from math import atan2, cos, sin

from car import Car
from myLibrary import *
from slider import Slider

# from payneW import PayneW
# from wavefront import Wavefront
from QLearning import QTable


pygame.init()
import sys


# pygame window definition
bgColor = (0, 0, 0)
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


backgroundImage = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
backgroundImage.set_colorkey((0, 0, 0))

roadRadius = 300
roadWidth = 50

pygame.draw.circle(
    backgroundImage,
    pygame.Color("White"),
    (WINDOW_HEIGHT // 2, WINDOW_HEIGHT // 2),
    roadRadius - roadWidth // 2,
    3,
)
pygame.draw.circle(
    backgroundImage,
    pygame.Color("White"),
    (WINDOW_HEIGHT // 2, WINDOW_HEIGHT // 2),
    roadRadius + roadWidth // 2,
    3,
)

valuesDict = {
    "Max Speed": 100,
    "Acceleration": 5,
    "Min Distance": 2000,
    "nb Car": 40,
    "Reaction Time": 20,
}

extremaValuesDict = {
    "Max Speed": (0, 200),
    "Acceleration": (0, 100),
    "Min Distance": (500, 5000),
    "nb Car": (1, 200),
    "Reaction Time": (1, 100),  # in frames
}

sliderList: list[Slider] = []
for i in range(len(valuesDict.keys())):
    sliderList.append(Slider(valuesDict, extremaValuesDict, i))

carList: list[Car] = []

carAngleList = [i * 360 / valuesDict["nb Car"] for i in range(valuesDict["nb Car"])]
for i in range(valuesDict["nb Car"]):
    carList.append((Car(valuesDict, roadRadius, i, carAngleList, carList)))

for car in carList:
    car.updateValues()
    car.initState()


isRunning = True
isDragging = False

nbSlider = len(valuesDict)
slidingId = 0

# keyboard slider control
selectedSliderId = 0
for i in range(nbSlider):
    sliderList[i].selected = i == selectedSliderId


# debug logic
debugDict = {}
debugDict["thinking"] = True

# PW logic

# payneW = PayneW(carList, valuesDict)

# wavefront logic

# wavefront = Wavefront(carList, valuesDict, roadRadius)

# qTable logic
qTable = QTable(debugDict, carList, valuesDict, roadRadius)


while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            # sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
                sys.exit()
            if event.key == pygame.K_SPACE:
                carList[0].stopped = not carList[0].stopped
            if event.key == pygame.K_q:
                isRunning = False
                sys.exit()

            if event.key == pygame.K_r:
                carList.clear()
                carAngleList = [
                    i * 360 / valuesDict["nb Car"] for i in range(valuesDict["nb Car"])
                ]
                for i in range(valuesDict["nb Car"]):
                    carList.append(
                        (Car(valuesDict, roadRadius, i, carAngleList, carList))
                    )
            if event.key == pygame.K_t:
                debugDict["thinking"] = not debugDict["thinking"]

            if event.key == pygame.K_j:
                selectedSliderId += 1
            if event.key == pygame.K_k:
                selectedSliderId -= 1

            selectedSliderId %= nbSlider
            for i in range(nbSlider):
                sliderList[i].selected = i == selectedSliderId

            mods = event.mod
            multiplier = 1
            if mods == 1:
                multiplier = 5
            if mods == 65:
                multiplier = 25
            if mods == 64:
                multiplier = 100

            if event.key == pygame.K_h:
                sliderList[selectedSliderId].addToValue(-1 * multiplier)

            if event.key == pygame.K_l:
                sliderList[selectedSliderId].addToValue(1 * multiplier)

        if event.type == pygame.MOUSEWHEEL:
            mousePos = pygame.mouse.get_pos()
            mouseScroll = event.y
            for slider in sliderList:
                slider.checkScroll(mousePos, mouseScroll)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            for i, slider in enumerate(sliderList):
                if slider.checkClick(mousePos):
                    pygame.mouse.get_rel()
                    isDragging = True
                    slidingId = i

        if event.type == pygame.MOUSEBUTTONUP:
            if isDragging:
                isDragging = False
                sliderList[slidingId].dragged = False

    # update values
    while len(carList) > round(valuesDict["nb Car"]):
        carList.pop()
        carAngleList.pop()

    while len(carList) < round(valuesDict["nb Car"]):
        firstCarAngle = degToRad(carAngleList[0])
        secondCarAngle = degToRad(carAngleList[-1])
        newAngle = radToDeg(
            atan2(
                (sin(firstCarAngle) + sin(secondCarAngle)) / 2,
                (cos(firstCarAngle) + cos(secondCarAngle)) / 2,
            )
        )
        carAngleList.append(newAngle)

        newSpeed = (carList[-1].speed + carList[0].speed) / 2

        carList.append(Car(valuesDict, roadRadius, len(carList), carAngleList, carList))
        carList[-1].speed = newSpeed

    for car in carList:
        car.updateValues()
        car.updatesIds()
        car.initState()

    # Game Loop

    display.fill((0, 0, 0))
    display.blit(backgroundImage, (0, 0))

    qTable.setActions()

    for car in carList:
        car.update()
        car.draw()

    qTable.learn()

    for slider in sliderList:
        slider.updateImage()
        slider.draw()

    # payneW.update()
    # wavefront.update()

    showDebugValues(display, debugDict)

    pygame.display.update()
    fpsClock.tick(FPS)
