#!/usr/bin/python2.7
import sudoku as su
import random, sys
from multiprocessing import Process, Queue, Manager
import multiprocessing as mp

su.Initial_population = 800
su.Litter_Size =8
su.Mortality_Rate = 75
su.Mutation_Rate = .0048
popMutation_Rate = 93.9

def generation(population):
        manager=Manager()
        bestscores = manager.list()
        pops = manager.list()
        try:
                rep = True
                while rep:
                        killsome = su.mortality(population)
                        makemore = su.reproduction(killsome)
                        newpop=[]
                        fits=[]
                        for pop in makemore:
                            if random.randint(0,100) <= popMutation_Rate:
                                mutie = su.mutate(pop)
                                newpop.append(mutie)
                            else:
                                newpop.append(pop)
                                for pop in newpop:
                                    if pop['fitness'] ==0:
                                        sol = su.combine(pop['puzzle_dict'])
                                        su.log(sol)
                                        rep=False
                                    else:
                                        fits.append(pop['fitness'])
                        best = sorted(fits[:6])
                        su.log(best)
                        bestscores.append(best)
                        pops.append(newpop)
                        which = min(bestscores[-4:])
                        where = bestscores.index(which)
                        population = pops[where]

                        rep=True
        except Exception as err:
                su.log(err)

    
def birth(puzzle):
    birth = su.reproduction(su.create_population(su.findBlanks(puzzle)))
    return birth


            
if __name__ =='__main__':

        population = birth(su.puzzle)
        for i in range(4):
                p = Process(target=generation, args = (population,))
                p.start()
                print p





            
       
