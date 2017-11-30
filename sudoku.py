import random, copy, time

#Variables
GenerationCount = 0
solution = []

### This is the puzzle to solve, with blank values = 0
puzzle = [[0,0,3,0,0,0,0,0,9],
          [7,0,0,2,0,4,8,0,0],
          [0,0,4,0,9,0,0,3,0],
          [3,0,7,1,0,0,0,0,0],
          [0,2,0,8,0,9,0,5,0],
          [0,0,0,0,0,3,7,0,2],
          [0,3,0,0,2,0,6,0,0],
          [0,0,9,3,0,1,0,0,5],
          [8,0,0,0,0,0,3,0,0]]

#Functions
def log(message):
   print message
   file('AutoReplication.log', 'a').write("%s:\t%s\n" % (time.asctime(), message))

def create_population(blanks):
   gen1 = []
   for i in range (Initial_population):
      individual = {"puzzle_dict":{}}
      for gene in blanks:
         individual["puzzle_dict"][gene] = random.randint(1,9)
      #individual["fitness"] = fitness_score(individual["puzzle_dict"])
      gen1.append(individual)
   return gen1

def fitness_score(genes):
   thisPuzzle = combine(genes)

   #loop through puzzle and count invalid values
   target_fitness = 0
   for row in range (9):
      for c in range (9):
        value = thisPuzzle[row][c]
        thisRow = list(thisPuzzle[row])
        thisCol = []
        for j in range(9):
            thisCol.append(thisPuzzle[j][c])
        mCol = int(c/3)
        mRow = int(row/3)
        thisBox = []
        for mR in range(3):
            for mC in range(3):
                thisBox.append(thisPuzzle[mRow*3 + mR][mCol*3+mC])
        thisCol.remove(value) # avoids double counting
        thisBox.remove(value) # avoids double counting
        thisRow.remove(value) # avoids double counting
        if value in thisRow or value in thisCol or value in thisBox:
            target_fitness += 1
   return target_fitness

def mutate(individual):
   for gene in individual["puzzle_dict"]:
      if random.randint(0,100) <= Mutation_Rate:
         individual["puzzle_dict"][gene] = random.randint(1,9)
   #individual["fitness"] = fitness_score(individual["puzzle_dict"])
   return individual

def mortality(population): #sort individuals (list by fitness score), kill off least fit
   sortedPop = sorted(population) #sorted function accepts any iterable, where list.sort does not
   cutOff = int(round(len(population) * ((100.0-Mortality_Rate)/100.0), 0))
   return sortedPop[:cutOff]

def reproduction(population):
   nextGen = []
   for i in range(len(population)/2):
      parent_1 = random.choice(population)
      parent_2 = random.choice(population)
##      while parent_1 == parent_2:
##         parent_2 = random.choice(population)

      for offspring in range(Litter_Size):
         newGenes = findBlanks(puzzle)
         for gene in newGenes:
            newGenes[gene] = random.choice((parent_1["puzzle_dict"][gene], parent_2["puzzle_dict"][gene]))
         individual = getNewIndividual(newGenes)
         nextGen.append(individual)
   return nextGen

def combine(genes):
   #combine individual (filled empty spaces) with existing puzzle to complete the 9x9 array (in combine function)
   thisPuzzle = copy.deepcopy(puzzle)
   for location in genes:
      value = genes[location]
      thisPuzzle[location[0]][location[1]] = value
   return thisPuzzle

def findBlanks(puzzle):
   #store location of blank values (ie, genes) as dictionary
   puzzle_dict = {}
   for row in range(len(puzzle)):
      for column in range(len(puzzle[row])):
         value = puzzle[row][column]
         if value == 0:
            puzzle_dict [row,column] = 0 #key is location, value is dummy value
   return puzzle_dict

def getNewIndividual(puzzle_dict):
   individual = {}
   individual["puzzle_dict"] = puzzle_dict
   individual["fitness"] = fitness_score(puzzle_dict) #key 1 is nested dictionary, key 2 is score, value is random
   return individual
