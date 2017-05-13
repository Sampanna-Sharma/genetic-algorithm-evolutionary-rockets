from tkinter import *
import time
import random
import math


ROCKET_WIDTH = 5
ROCKET_HEIGHT = 30
NUMBER_OF_POPULATION = 20
LIFE_SPAN = 60
TARGET_X = 290
TARGET_Y = 50
MAX_FITNESS = 0
ROCK_X1 = 150
ROCK_Y1 = 250
ROCK_X2 = 350
ROCK_Y2 = 270
COLOR = ['red', 'blue', 'green']


#helper class

class DNA:
    def __init__(self):
        self.accX = [random.randint(-3, 3) for _ in range(LIFE_SPAN)]
        self.accY = [random.randint(-2, 1) for _ in range(LIFE_SPAN)]
        self.velX = []
        self.velY = []
        for i in range(len(self.accX)):
            if i == 0:
                self.velX.append(self.accX[i])
                self.velY.append(self.accY[i])
            else:
                self.velX.append(self.velX[i-1]+self.accX[i])
                self.velY.append(self.velY[i-1] + self.accY[i])


class Rocket(DNA):
    def __init__(self, x, y):
        DNA.__init__(self)
        self.x1 = x
        self.y1 = y
        self.x2 = self.x1 + ROCKET_WIDTH
        self.y2 = self.y1 + ROCKET_HEIGHT


def calcfitness(orga):
    fitness = []
    fitnesss = []
    for i in range(len(orga)):
        if orga[i].velX == [0]*LIFE_SPAN and orga[i].velY == [0]*LIFE_SPAN:
            fitness.append(0)
        else:
            dis =math.pow((TARGET_X -orga[i].x1)*(TARGET_X -orga[i].x1)+(TARGET_Y -orga[i].y1)*(TARGET_Y -orga[i].y1), 1)
            fitness.append(1/(dis))

    fitt = fitness.copy()
    fitness.sort()

    for j in range(len(fitness)):
        fitnesss.append((fitt[j]/fitness[len(fitness)-1])*100)

    print(fitnesss)

    return fitnesss








def crossover(parentA, parentB):
    child = Rocket(250, 450)
    mid = random.randint(0, LIFE_SPAN)
    for i in range(LIFE_SPAN):
        if random.random() > 0.05:
            if i > mid:
                child.accX[i] = parentA.accX[i]
                child.accY[i] = parentA.accY[i]
            else:
                child.accX[i] = parentB.accX[i]
                child.accY[i] = parentB.accY[i]
        else:
            pass
    child.velX = []
    child.velY = []
    for i in range(len(child.accX)):
        if i == 0:
            child.velX.append(child.accX[i])
            child.velY.append(child.accY[i])
        else:
            child.velX.append(child.velX[i - 1] + child.accX[i])
            child.velY.append(child.velY[i - 1] + child.accY[i])


    return child



def mattingpool(Rocketss):
    mattingpools = []

    fit = calcfitness(Rocketss)
    for i in range(len(Rocketss)):
        for _ in range(int(fit[i])):
            mattingpools.append(Rocketss[i])

    return mattingpools


def childrens(mattingpoolss):
    ans = []
    for i in range(NUMBER_OF_POPULATION):

        j = random.choice(mattingpoolss)
        k = random.choice(mattingpoolss)
        ans.append(crossover(j, k))
    return ans



if __name__ == "__main__":
    root = Tk()
    root.title("Evolutionary Rockets")
    canvas = Canvas(root, width=500, height=500)
    canvas.pack()
    Rock = canvas.create_rectangle(ROCK_X1, ROCK_Y1, ROCK_X2, ROCK_Y2, fill="black")
    Taget = canvas.create_rectangle(150, 5, TARGET_X + 80, TARGET_Y + 10, fill='yellow')
    Rockets = [Rocket(250, 450) for _ in range(NUMBER_OF_POPULATION)]
    Draw_Rockets = [canvas.create_rectangle(Rockets[i].x1, Rockets[i].y1, Rockets[i].x2, Rockets[i].y2, fill=random.choice(COLOR))
                    for i in range(NUMBER_OF_POPULATION)]


    # root.mainloop()
    j = 0

    while True:
        for i in range(NUMBER_OF_POPULATION):
            canvas.move(Draw_Rockets[i], Rockets[i].velX[j], Rockets[i].velY[j])
            Rockets[i].x1 = Rockets[i].x1 +Rockets[i].velX[j]
            Rockets[i].y1 = Rockets[i].y1 +Rockets[i].velY[j]
            if Rockets[i].x1 > ROCK_X1 and Rockets[i].x1 < ROCK_X2 and Rockets[i].y1 > ROCK_Y1 and Rockets[i].y1 < ROCK_Y2:
                Rockets[i].velX = [0]*LIFE_SPAN
                Rockets[i].velY = [0]*LIFE_SPAN


        root.update()
        time.sleep(0.1)
        j += 1

        if j >= LIFE_SPAN:
            j = 0
            canvas.delete("all")
            Taget = canvas.create_rectangle(150, 5, TARGET_X+80, TARGET_Y+10, fill='yellow')
            Rock = canvas.create_rectangle(ROCK_X1, ROCK_Y1, ROCK_X2, ROCK_Y2, fill="black")


            Rockets = childrens(mattingpool(Rockets))
            Draw_Rockets = [canvas.create_rectangle(Rockets[i].x1, Rockets[i].y1, Rockets[i].x2, Rockets[i].y2, fill=random.choice(COLOR))
                            for i in range(NUMBER_OF_POPULATION)]
