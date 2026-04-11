from car import Car


class PayneW:
    def __init__(self, carList: list[Car], valueDict) -> None:
        self.carList = carList
        self.valueDict = valueDict

        self.carIdAt0 = 0

        self.carsAround0 = [carList[i] for i in range(-1, 2)]

    def getClosestCarFrom0(self):
        nbCar = len(self.carList)

        closestId = 0
        closestAngle = self.carList[0].angle
        for i in range(nbCar):
            currentCar = self.carList[i]
            currentAngle = currentCar.angle
            if currentAngle < closestAngle or abs(360 - currentAngle) < closestAngle:
                closestAngle = min(currentAngle, abs(360 - currentAngle))
                closestId = currentCar.carId

        return closestId

    def updateCarsAround0(self):
        nbCar = len(self.carList)
        closestCarIdTo0 = self.getClosestCarFrom0()
        for i in range(-1, 2):
            self.carsAround0[i + 1] = self.carList[(closestCarIdTo0 + i) % nbCar]

    def getAverageSpeedAt0(self):
        speedSum = 0
        for car in self.carsAround0:
            speedSum += car.getSpeed()
        return speedSum / 3

    def update(self):
        self.updateCarsAround0()
