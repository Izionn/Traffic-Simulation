import numpy as np
from myLibrary import *
from car import Car


class QTable:
    def __init__(
        self,
        debugDict,
        carList: list[Car],
        valueDict,
        roadRadius,
    ) -> None:

        self.debugDict = debugDict
        self.carList = carList
        self.valueDict = valueDict
        self.roadRadius = roadRadius

        # dims -> range / interval:
        #   - self.speed -> [0, 130] / 10
        #   - next.speed -> [0, 130] / 10
        #   - self.dist -> [0, 1000] / 100

        # actions:
        #   - 0 : gaz
        #   - 1 : cruise
        #   - 2 : break

        self.dimNb = 3
        self.dimList = [14, 14, 11]
        self.actionNb = 3

        self.stateSelfSpeedValues = np.arange(start=0, stop=131, step=10)
        self.stateNextSpeedValues = np.arange(start=0, stop=131, step=10)
        self.stateDistValues = np.arange(start=0, stop=1001, step=100)

        self.stateSelfSpeedInterval = 10
        self.stateNextSpeedInterval = 10
        self.stateDistInterval = 100

        self.qTable = np.zeros(self.dimList + [self.actionNb])

        self.gamma = 0.9
        self.alpha = 0.01
        self.epsilon = 1
        self.epsilonDecay = 0.99999
        self.epsilonMin = 0.01

        self.debugDict["epsilon"] = self.epsilon

    def setActions(self):
        nbCar = len(self.carList)
        for carId in range(nbCar):

            currentCar = self.carList[carId]

            if np.random.rand() > self.epsilon:

                state = currentCar.state
                stateIndices = self.discretizeState(state)

                currentQValues = self.qTable[*stateIndices]
                optimalAction = currentQValues.argmax()
                currentCar.action = optimalAction.item()

            else:
                randomAction = np.random.randint(0, 3)
                currentCar.action = randomAction

    def learn(self):
        nbCar = len(self.carList)
        for carId in range(nbCar):
            currentCar = self.carList[carId]
            nextCar = self.carList[(carId + 1) % nbCar]

            state = currentCar.state

            newStateSelfSpeed = currentCar.speed
            newstateNextSpeed = nextCar.speed
            newstateDist = abs(nextCar.angle - currentCar.angle) * self.roadRadius

            newState = np.array([newStateSelfSpeed, newstateNextSpeed, newstateDist])

            reward = newStateSelfSpeed

            action = currentCar.action

            self.updateQ(state, action, reward, newState)

            currentCar.state = newState

        self.epsilon = max(self.epsilon * self.epsilonDecay, self.epsilonMin)
        self.debugDict["epsilon"] = round(self.epsilon, 2)

    def updateQ(self, state, action, reward, newState):
        indexState = self.discretizeState(state)
        indexState = self.discretizeState(newState)
        self.qTable[*indexState, action] = self.qTable[*indexState, action] * (
            1 - self.alpha
        ) + self.alpha * (reward + self.gamma * self.qTable[*indexState].max())
        return

    def discretizeState(self, state):
        selfSpeed, nextSpeed, dist = state

        discreteSelfSpeed = closestValInArray(selfSpeed, self.stateSelfSpeedValues)
        discreteNextSpeed = closestValInArray(nextSpeed, self.stateNextSpeedValues)
        discreteDist = closestValInArray(dist, self.stateDistValues)

        indexSelfSpeed = discreteSelfSpeed // self.stateSelfSpeedInterval
        indexNextSpeed = discreteNextSpeed // self.stateNextSpeedInterval
        indexDist = discreteDist // self.stateDistInterval

        return np.array([indexSelfSpeed, indexNextSpeed, indexDist])
