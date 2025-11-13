import pygame

pygame.init()


class Slider:
    def __init__(self, valuesDict, extremaValuesDict, id) -> None:
        self.display = pygame.display.get_surface()
        self.displaySize = self.display.get_size()

        self.valuesDict = valuesDict
        self.extremaValuesDict = extremaValuesDict
        self.id = id
        self.key = list(valuesDict.keys())[self.id]

        self.width, self.height = 400, 100
        self.posX = self.displaySize[0] - self.width - 10
        self.posY = self.id * self.height + 5

        self.image = pygame.Surface((self.width, self.height))
        self.bgColor = pygame.Color(20, 20, 20)
        self.barColor = pygame.Color(100, 100, 100)
        self.sliderColor = pygame.Color(255, 255, 255)

        self.value = self.valuesDict[self.key]
        self.minValue = self.extremaValuesDict[self.key][0]
        self.maxValue = self.extremaValuesDict[self.key][1]
        self.step = (self.maxValue - self.minValue) / 100

        self.fontColor = pygame.Color(150, 150, 150)
        self.font = pygame.font.Font(r"./FiraCodeNerdFontMono-Light.ttf", 24)

        self.nameSurf = self.font.render(
            self.key,
            True,
            (255, 255, 255),
        )
        self.maxValueFontSurf = self.font.render(
            str(self.maxValue), True, self.fontColor
        )
        self.minValueFontSurf = self.font.render(
            str(self.minValue), True, self.fontColor
        )

        # slider constants
        self.barMargin = 20
        self.barLength = self.width - 2 * self.barMargin
        self.barPosY = round(3 * self.height / 4)
        self.barHeight = 10
        self.centerX = self.width // 2
        self.sliderRadius = 10

        # click and drag slider logic
        self.sliderPosX = 0
        self.sliderPosY = round(round(3 * self.height / 4) + 10 / 2)
        self.dragged = False

        self.updateImage()

    def checkClick(self, mousePos):

        deltaX = self.posX + self.sliderPosX - mousePos[0]
        deltaY = self.posY + self.sliderPosY - mousePos[1]

        if deltaX**2 + deltaY**2 < self.sliderRadius**2:
            self.dragged = True
            return True

        return False

    def slide(self, deltaMouse):
        deltaMouseX = deltaMouse[0]

    def checkScroll(self, mousePos, mouseScroll):
        mouseX, mouseY = mousePos
        if (
            self.posX <= mouseX <= self.posX + self.width
            and self.posY <= mouseY <= self.posY + self.height
        ):
            self.value += self.step * mouseScroll
            if self.value > self.maxValue:
                self.value = self.maxValue
            if self.value < self.minValue:
                self.value = self.minValue

            self.valuesDict[self.key] = self.value

            self.updateImage()

    def updateImage(self):

        self.sliderPosX = round(
            self.barMargin
            + self.barHeight / 2
            + (self.barLength - self.barHeight)
            * (self.value - self.minValue)
            / (self.maxValue - self.minValue)
        )

        bgRect = pygame.Rect(0, 0, self.width, self.height - 5)
        barRect = pygame.Rect(
            self.barMargin, self.barPosY, self.barLength, self.barHeight
        )

        pygame.draw.rect(self.image, self.bgColor, bgRect, border_radius=20)
        pygame.draw.rect(self.image, self.barColor, barRect, border_radius=20)
        pygame.draw.circle(
            self.image,
            self.sliderColor,
            (self.sliderPosX, round(self.barPosY + self.barHeight / 2)),
            self.barHeight,
        )

        namePos = (self.centerX - self.nameSurf.get_size()[0] // 2, 5)
        valuesPosY = round(
            self.barPosY - self.barHeight * 0.75 - self.maxValueFontSurf.get_size()[1]
        )
        maxValuePos = (
            self.width - self.maxValueFontSurf.get_size()[0] - self.barMargin,
            valuesPosY,
        )
        minValuePos = (self.barMargin, valuesPosY)

        currentValueText = self.font.render(
            str(round(self.value, 1)), True, (255, 255, 255)
        )
        currentValuePos = (self.width - currentValueText.get_size()[0]) // 2

        self.image.blit(self.nameSurf, namePos)
        self.image.blit(self.maxValueFontSurf, maxValuePos)
        self.image.blit(self.minValueFontSurf, minValuePos)
        self.image.blit(currentValueText, (currentValuePos, valuesPosY))

    def draw(self):
        self.display.blit(
            self.image,
            (self.posX, self.posY),
        )


myDict = {
    "key1": 1,
    "key2": 2,
    "key3": 3,
    "key4": 4,
    "key5": 5,
}
