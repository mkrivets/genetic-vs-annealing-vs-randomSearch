import numpy as np


class Chromosome:
    xMin = -30
    xMax = 30
    yMin = -10
    yMax = 10

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def fitness(self):
        return -self.X * (np.sin(np.sqrt(abs(self.X)))) + self.Y * np.cos(np.sqrt(abs(self.Y)))

    def get_info(self):
        return self.X, self.Y, self.fitness()

    def gene_X_mutation(self):
        randNum = np.random.uniform(self.xMin / 3, self.xMax / 3)
        if ((self.X + randNum >= self.xMin) and (self.X + randNum <= self.xMax)):  # to avoid extending beyond
            self.X += randNum
        else:
            if ((self.X + (randNum / 3) >= self.xMin) and (self.X + (randNum / 3) <= self.xMax)):
                self.X += randNum / 3
            else:
                self.X -= randNum

    def gene_Y_mutation(self):
        randNum = np.random.uniform(self.yMin / 3, self.yMax / 3)
        if ((self.Y + randNum >= self.yMin) and (self.Y + randNum <= self.yMax)):  # to avoid extending beyond
            self.Y += randNum
        else:
            if ((self.Y + (randNum / 3) >= self.yMin) and (self.Y + (randNum / 3) <= self.yMax)):
                self.Y += randNum / 3
            else:
                self.Y -= randNum


class Population:
    def __init__(self, number):
        self.number = number
        self.chromosomeList = []
        self.chromosomeListOriginal = []

    def add_chromosome(self, chromosome):
        self.chromosomeList.append(chromosome)
        self.chromosomeListOriginal.append(chromosome)

    def add_chromosomeList(self, chList):
        self.chromosomeList = chList
        self.chromosomeListOriginal = chList

    def set_random_chromosomeList(self, xMin, xMax, yMin, yMax):
        for i in range(0, 4):
            self.chromosomeList.append(Chromosome(np.random.uniform(xMin, xMax), np.random.uniform(yMin, yMax)))
        self.chromosomeListOriginal = self.chromosomeList

    def get_chromosomeList(self):
        return self.chromosomeList

    def get_chromosomeListOriginal(self):
        return self.chromosomeListOriginal

    def worst_chromosome(self):
        maxFitness = self.chromosomeList[0].fitness()
        worst = self.chromosomeList[0]
        for ch in self.chromosomeList:
            if ch.fitness() > maxFitness:
                maxFitness = ch.fitness()
                worst = ch
        return worst

    def selection(self):
        self.chromosomeList.remove(self.worst_chromosome())

    # from selected three
    def best_to_worst_order(self):
        worst = self.worst_chromosome()
        self.chromosomeList.remove(worst)
        self.chromosomeList.append(worst)  # the worst to the end of the list
        if self.chromosomeList[0].fitness() > self.chromosomeList[1].fitness():
            self.chromosomeList[0], self.chromosomeList[1] = self.chromosomeList[1], self.chromosomeList[0]

    def best_chromosome_after_selection(self):
        self.best_to_worst_order()
        return self.chromosomeList[0]

    def crossover(self):
        self.best_to_worst_order()
        ch1 = Chromosome(self.chromosomeList[1].X, self.chromosomeList[0].Y)
        ch2 = Chromosome(self.chromosomeList[2].X, self.chromosomeList[0].Y)
        ch3 = Chromosome(self.chromosomeList[0].X, self.chromosomeList[1].Y)
        ch4 = Chromosome(self.chromosomeList[0].X, self.chromosomeList[2].Y)
        self.chromosomeList = [ch1, ch2, ch3, ch4]

    def mutations(self):
        self.chromosomeList[0].gene_X_mutation()
        self.chromosomeList[1].gene_X_mutation()
        self.chromosomeList[2].gene_Y_mutation()
        self.chromosomeList[3].gene_Y_mutation()
