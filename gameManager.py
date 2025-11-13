import pygame

from car import Car
from slider import Slider


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
    "Acceleration": 20,
    "Min Distance": 300,
    "nb Car": 10,
    "Reaction Time": 20,
}
extremaValuesDict = {
    "Max Speed": (0, 200),
    "Acceleration": (0, 100),
    "Min Distance": (100, 1000),
    "nb Car": (1, 200),
    "Reaction Time": (1, 100),  # in frames
}

sliderList: list[Slider] = []
for i in range(len(valuesDict.keys())):
    sliderList.append(Slider(valuesDict, extremaValuesDict, i))

carList: list[Car] = []
nbCar = valuesDict["nb Car"]
carAngleList = [i * 360 / nbCar for i in range(nbCar)]
for i in range(nbCar):
    carList.append((Car(valuesDict, roadRadius, i, carAngleList, carList)))

isRunning = True
isDragging = False
slidingId = 0

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
                carList = []
                carAngleList = [i * 360 / nbCar for i in range(nbCar)]
                for i in range(nbCar):
                    carList.append(
                        (Car(valuesDict, roadRadius, i, carAngleList, carList))
                    )

        if event.type == pygame.MOUSEWHEEL:
            mousePos = pygame.mouse.get_pos()
            mouseScroll = event.y
            for slider in sliderList:
                slider.checkScroll(mousePos, mouseScroll)

                nbCar = round(valuesDict["nb Car"])

            while len(carList) > round(valuesDict["nb Car"]):
                carList.pop()
                carAngleList.pop()
            while len(carList) < round(valuesDict["nb Car"]):
                carAngleList.append(carAngleList[0] - 5)
                carList.append(
                    Car(valuesDict, roadRadius, len(carList), carAngleList, carList)
                )
                carList[-1].setSpeed(carList[0].getSpeed())

            for car in carList:
                car.updateValues()
                car.updatesIds()

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

        if event.type == pygame.KEYUP:
            pass

    # Game Loop

    if isDragging:
        deltaMouse = pygame.mouse.get_rel()
        sliderList[slidingId]

    display.fill((0, 0, 0))
    display.blit(backgroundImage, (0, 0))

    for car in carList:
        car.update()
        car.draw()

    for slider in sliderList:
        slider.draw()

    pygame.display.update()
    fpsClock.tick(FPS)
