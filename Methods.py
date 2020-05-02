import random as rnd

def chance(thresh):
    r = rnd.randint(0, 1000)
    if r < thresh * 1000:
        return 1
    else:
        return 0


def dailyInfect(I, pop, IR, interactions, totalpop):
    for i in [p for p in pop if p.type == 'S']:
        # I = [p for p in pop if p.type == 'I']
        numInfectEncount = 0
        for j in range(interactions):
            if chance(I / totalpop):
                numInfectEncount += 1
        if chance(numInfectEncount * IR):
            i.type = 'I'
            # I[rnd.randint(0, len(I)-1)].numInfected += 1
            num = rnd.choice([p for p in pop if p.type == 'I']).id
            # pop[rnd.choice([p for p in pop if p.type == 'I']).id].numInfected += 1
            pop[num].numInfected += 1
            # print(pop[num].numInfected)
    return pop


def addDay(pop):
    I = [p for p in pop if p.type == 'I']
    for i in I:
        i.daysSick += 1
    return pop


def removed(pop, dailyDeathRate, rLen):
    I = [p for p in pop if p.type == 'I']
    for i in I:
        if i.daysSick >= rLen:
            if chance(dailyDeathRate):
                i.type = 'D'
            else:
                i.type = 'R'
            # to be added is instead added to death
    return pop


def daily_reproduction_number(infected, rLen):
    r = []
    for i in infected:
        try:
            rate = i.numInfected / i.daysSick
        except ZeroDivisionError:
            rate = 0
        est = i.numInfected + rate * (rLen - i.daysSick)
        r.append(est)
    if r:
        return r
    else:
        return [0]
