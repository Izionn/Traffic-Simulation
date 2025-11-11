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

        self.updateImage()

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
        barMargin = 20
        barLength = self.width - 2 * barMargin
        barPosY = round(3 * self.height / 4)
        barHeight = 10  # used as radius for the slider
        centerX = self.width // 2

        sliderPosX = round(
            barMargin
            + barHeight / 2
            + (barLength - barHeight)
            * (self.value - self.minValue)
            / (self.maxValue - self.minValue)
        )

        bgRect = pygame.Rect(0, 0, self.width, self.height - 5)
        barRect = pygame.Rect(barMargin, barPosY, barLength, barHeight)

        pygame.draw.rect(self.image, self.bgColor, bgRect, border_radius=20)
        pygame.draw.rect(self.image, self.barColor, barRect, border_radius=20)
        pygame.draw.circle(
            self.image,
            self.sliderColor,
            (sliderPosX, round(barPosY + barHeight / 2)),
            barHeight,
        )

        namePos = (centerX - self.nameSurf.get_size()[0] // 2, 5)
        valuesPosY = round(
            barPosY - barHeight * 0.75 - self.maxValueFontSurf.get_size()[1]
        )
        maxValuePos = (
            self.width - self.maxValueFontSurf.get_size()[0] - barMargin,
            valuesPosY,
        )
        minValuePos = (barMargin, valuesPosY)

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
