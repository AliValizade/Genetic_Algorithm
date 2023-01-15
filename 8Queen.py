# 8-QUEEN with Genetic Algorithm
import math 
import itertools
import random

# First population production
def currentPopulation(population_size):
  randGen = itertools.permutations([0, 1, 2, 3, 4, 5, 6, 7], r=None)
  start = random.randint(0, 40320 - population_size)
  stop = start + population_size
  return list(itertools.islice(randGen, start, stop))

# Calculate the number of collisions available for a Queen
def collisionQueens(index, genum):
  col = index
  row = genum[index]
  collisin = 0
  for i in range(len(genum)):
    if i == col:
      continue
    if math.fabs(i-col) == math.fabs(genum[i] - row):
      collisin += 1
  return collisin

# Calculating the total number of hits for a genome
def sumOfCollision(genum):
  sum = 0
  for i in range(len(genum)):
    sum += collisionQueens(i, genum)
  return sum

# Calculating fitness for a genome 
def genumFitness(genum):
  collision = sumOfCollision(genum)
  if collision > 0:
    return 1 / collision
  else:
    return 2

# Random selection of 5 parents for reproduction
def selection(population, num):
  randomlist = random.sample(range(0, len(population)), num)
  selected = []
  for i in randomlist:
    selected.append(population[i])
  return selected

# Selection of 2 parents with high fitness from random selections
def get_two_parents(population):
  population.sort(reverse=True, key=genumFitness)
  # print(population)
  return population[0:2]

# Production of 2 children with two selected parents
def cross_over(parent1, parent2):
  parent1 = list(parent1)
  parent2 = list(parent2)
  position = random.randint(1,6)
  # print("Cross over Position = " , position)
  child1 = parent1[0:position]
  child2 = parent2[0:position]
  for i in range(len(parent1)):
    if parent1[i] not in child2:
      child2.append(parent1[i])
    if parent2[i] not in child1:
      child1.append(parent2[i])
  child1 = tuple(child1)
  child2 = tuple(child2)
  return [child1, child2]

# Mutation with a 15% chance
def mutation(childs):
  mutated =[]
  for child in childs:
    prob = random.randint(1, 100)
    # print("Mutation Prob = ", prob)
    if prob < mutation_prob:
      mutated.append(mutate(child))
    else:
      mutated.append(child)
  return mutated

def mutate(genum):
  position1 = random.randint(0, len(genum) - 1)
  position2 = random.randint(0, len(genum) - 1)
  # print("Mutation Pos = ", position1, " , " , position2)
  genum = list(genum)
  temp = genum[position1]
  genum[position1] = genum[position2]
  genum[position2] = temp
  genum = tuple(genum)
  return genum

# replacing the generation
def  replacement(population, childs):
  population.sort(reverse=True, key=genumFitness)
  population[-1] = childs[0]
  population[-2] = childs[1]
  if genumFitness(childs[0]) == 2:
    return (1, population)
  if genumFitness(childs[1]) == 2 :
    return (2, population)
  return (0, population)

# Print a genome on a chessboard in the console
def printGenum(genum):
  for i in range(8):
    print('|', end='')
    for j in range(8):
      if j == genum[i]:
        print(' Q |', end='')
      else:
        print('   |', end='')
    print()
    print('---------------------------------')

population_size = 150
select_random = 8
mutation_prob = 15
pop = currentPopulation(population_size)
rounds = 2000
TOTAL_ROUNDS = rounds

while rounds > 0:
  selected = selection(pop, select_random)  
  parents = get_two_parents(selected)
  childs = cross_over(parents[0], parents[1])
  childs = mutation(childs)
  done, pop = replacement(pop, childs)
  if done == 1:
    print("Best 5 answer after {0} iterations:".format(TOTAL_ROUNDS - rounds))
    pop.sort(reverse=True, key=genumFitness)
    print(pop[0:5])
    print("Best answer:")
    print(childs[0])
    print()
    printGenum(childs[0])
    break
  if done == 2:
    print("Best 5 answer after {0} iterations:".format(TOTAL_ROUNDS - rounds))
    pop.sort(reverse=True, key=genumFitness)
    print(pop[0:5])
    print("Best answer:")
    print(childs[1])
    print()
    printGenum(childs[1])
    break
  rounds = rounds - 1

