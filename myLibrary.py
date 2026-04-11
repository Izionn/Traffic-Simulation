from math import pi
import pygame


def degToRad(deg):
    return ((deg / 180) * pi) % (2 * pi)


def radToDeg(rad):
    return (rad * 180 / pi) % (360)


def closestValInArray(x, array):
    closestVal = array[0]
    closestDist = abs(x - array[0])
    for y in array:
        if abs(x - y) < closestDist:
            closestVal = y
            closestDist = abs(x - y)
    return closestVal


def showDebugValues(display, debugDict):
    fontSize = 12
    font = pygame.font.Font(r"./FiraCodeNerdFontMono-Light.ttf", fontSize)

    nbRows = len(debugDict)
    rowsList = []
    maxRowWidth = 0
    for key in debugDict.keys():
        text = f'"{key}" : {debugDict[key]}'
        rowSurf = font.render(text, True, "#808080")
        rowsList.append(rowSurf)

        if rowSurf.get_width() > maxRowWidth:
            maxRowWidth = rowSurf.get_width()

    fontSurf = pygame.Surface((maxRowWidth, fontSize * nbRows))
    fontSurf.fill((0, 0, 0))
    for i in range(nbRows):
        fontSurf.blit(rowsList[i], (0, i * fontSize))

    display.blit(fontSurf, (0, 0))
