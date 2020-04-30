import matplotlib.pyplot as plt
import numpy as np
import random as rnd
from Person import Person

def chance(thresh):
    r = rnd.randint(0, 1000)
    if r < thresh * 1000:
        return 1
    else:
        return 0


def dailyInfect(I, pop):
    for i in [p for p in pop if p.type == 'S']:
        numInfectEncount = 0
        for j in range(interactions):
            if chance(I / totalpop):
                numInfectEncount += 1
        if chance(numInfectEncount * IR):
            i.type = 'I'
    return pop


def addDay(pop):
    I = [p for p in pop if p.type == 'I']
    for i in I:
        i.daysSick += 1
    return pop


def removed(pos, pop, D):
    I = [p for p in pop if p.type == 'I']
    for i in I:
        if i.daysSick >= rLen:
            i.type = 'R'
            if chance(dailyDeathRate): D += 1
            # to be added is instead added to death
    return pop, D


t = np.arange(365)
S = np.zeros(t.size)
I = np.zeros(t.size)
R = np.zeros(t.size)
# D = np.zeros(t.size)

factor = 10 ** 6

#  https://ourworldindata.org/coronavirus?country=USA
#  Case fatality rate as of April 29th is 5.76. This number is not super
#  helpful as our model is going daily.
CFR = 0.0576
#  Infection fatality rate as of April 29th is unknown (maybe)

#  https://www.worldometers.info/coronavirus/coronavirus-death-toll/
#  number of daily deaths as of April 29th / number of active cases as of
#  April 29th
dailyDeathRate = 6365 / 843987

#  https://www.who.int/docs/default-source/coronaviruse/who-china-joint-mission-on-covid-19-final-report.pdf#:~:text=Using20available20preliminary20data2C,severe20or20critical20disease.
#  Rough esimate of time to recover is 2 weeks for mild and 3-6 for severe.
#  Since I am including percentage of death I will use 3 weeks.
rLen = 21

#  https://www.worldometers.info/coronavirus/country/us/
#  so I will be using a crude Infection rate as it is #cases/population as
#  of April 29th. This obvsiously will not give an accurate representation
#  of percentage getting infection when in contact with someone who has it.
#  Although, in terms of comparsion between scenerios this will not play a
#  role in that effect.
# IR = 1048834 / (328.2 * 10**6)  # roughly .3 chance to get virus
IR = .01

#  https://www.researchgate.net/figure/Daily-average-number-of-contacts-per-person-in-age-group-j-The-average-number-of_fig2_228649013
#  Interactions per day (estimated)
interactions = 20
#  Now because of social distancing I will reduce this number
interactions = int(interactions / 2)

S[0] = 327
I[0] = 1
R[0] = 0
D = 0

totalpop = S[0] + I[0] + R[0] - D
pop = [Person('S', 0) for i in range(int(totalpop))]
pop[len(pop) - 1].type = 'I'
# print(sum([p.type == 'I' for p in pop]))

#
for i in t:
    S[i] = sum([p.type == 'S' for p in pop])
    I[i] = sum([p.type == 'I' for p in pop])
    R[i] = sum([p.type == 'R' for p in pop])
    pop = addDay(pop)
    pop = dailyInfect(I[i], pop)
    pop, D = removed(i, pop, D)

print(S)
print(I)
print(R)
print(D)

plt.plot(t, S, 'b', label='S')
plt.plot(t, I, 'r', label='I')
plt.plot(t, R, 'g', label='R')
plt.fill_between(t, I, color='r')
plt.legend()
plt.title('SIR Model')
plt.xlabel("Time (days)")
plt.ylabel("# of Persons")
plt.show()

# plt.style.use('classic')
# fig, ax = plt.subplots()
# ax.plot(t, S, label='S')
# ax.plot(t, I, label='I')
# ax.plot(t, R, label='R')
# ax.axis('time(days)')
# leg = ax.legend()
# plt.show()
