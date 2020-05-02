import matplotlib.pyplot as plt
import numpy as np
import random as rnd
from Person import Person
import Methods as M




t = np.arange(365)
S = np.zeros(t.size)
I = np.zeros(t.size)
R = np.zeros(t.size)
D = np.zeros(t.size)
reproduction_number = np.zeros(t.size)
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
# IR = 1048834 / (328.2 * 10**6)  # roughly .3 chance to get virus. This gave inaccurate results.
# 0.02 was chosen because it resulted in the reproductive number very closely resembling that of Covid-19 which is
# around 2.0
IR = .015

#  https://www.researchgate.net/figure/Daily-average-number-of-contacts-per-person-in-age-group-j-The-average-number-of_fig2_228649013
#  Interactions per day (estimated)
interactions = 20
#  Now because of social distancing I will reduce this number
interactions = int(interactions / 2)

S[0] = 327
I[0] = 1
R[0] = 0
D[0] = 0

totalpop = S[0] + I[0] + R[0] - D[0]
pop = [Person(i, 'S') for i in range(int(totalpop))]
pop[len(pop) - 1].type = 'I'


# print(sum([p.type == 'I' for p in pop]))


def SIR_Model(S, I, R, D, reproduction_number, dailyDeathRate, rLen, IR, interactions, pop):
    pop = [Person(i, 'S') for i in range(int(totalpop))]
    pop[len(pop) - 1].type = 'I'
    for i in t:
        S[i] = sum([p.type == 'S' for p in pop])
        I[i] = sum([p.type == 'I' for p in pop])
        R[i] = sum([p.type == 'R' for p in pop])
        D[i] = sum([p.type == 'D' for p in pop])
        pop = M.addDay(pop.copy())
        pop = M.dailyInfect(I[i], pop.copy(), IR, interactions, totalpop)
        pop = M.removed(pop.copy(), dailyDeathRate, rLen)
        l = M.daily_reproduction_number([p for p in pop if p.type == "I"], rLen)
        reproduction_number[i] = np.average(l)
    return S, I, R, D, reproduction_number, pop


def infection_rate_subplots(S, I, R, D, reproduction_number, pop):
    # running model with different infection rates
    n = 1
    for i in np.arange(0.01, 0.02, 0.001):
        S1, I1, R1, D1, reproduction_number1, pop1 = SIR_Model(S.copy(), I.copy(), R.copy(), D.copy(), reproduction_number.copy(), dailyDeathRate, rLen,
                                                               i, interactions, pop.copy())
        plt.subplot(2, 5, n)
        plt.plot(t, S1, 'b', label='S')
        plt.plot(t, I1, 'r', label='I')
        plt.plot(t, R1, 'g', label='R')
        plt.plot(t, D1, 'black', label='D')
        # plt.fill_between(t, I, color='r')
        plt.legend()
        plt.title("SIRD Model, IR=%.3f" % i)
        plt.xlabel("Time (days)")
        plt.ylabel(r"# of Persons $/10^6$")
        plt.text(250, 250, "R = %.3f" % (np.average([k for k in reproduction_number1 if k > 0])), fontsize=10)
        plt.text(250, 230, "deaths = %.0f" % (D1[len(D) - 1]))
        n += 1
    plt.show()


def interactions_subplots(S,I,R,D, reproduction_number, pop):
    # running model with different number of interactions
    n = 1
    for i in np.arange(5,15):
        S1, I1, R1, D1, reproduction_number1, pop1 = SIR_Model(S.copy(), I.copy(), R.copy(), D.copy(), reproduction_number.copy(), dailyDeathRate, rLen,
                                                               IR, i, pop.copy())
        plt.subplot(2, 5, n)
        plt.plot(t, S1, 'b', label='S')
        plt.plot(t, I1, 'r', label='I')
        plt.plot(t, R1, 'g', label='R')
        plt.plot(t, D1, 'black', label='D')
        # plt.fill_between(t, I, color='r')
        plt.legend()
        plt.title("SIRD Model, interactions=%.0f" % i)
        plt.xlabel("Time (days)")
        plt.ylabel(r"# of Persons $/10^6$")
        plt.text(250, 250, "R = %.3f" % (np.average([k for k in reproduction_number1 if k > 0])), fontsize=10)
        plt.text(250, 230, "deaths = %.0f" % (D1[len(D) - 1]))
        n += 1
    plt.show()


infection_rate_subplots(S.copy(), I.copy(), R.copy(), D.copy(), reproduction_number.copy(), pop.copy())
interactions_subplots(S.copy(), I.copy(), R.copy(), D.copy(), reproduction_number.copy(), pop.copy())
S, I, R, D, reproduction_number, pop = SIR_Model(S, I, R, D, reproduction_number, dailyDeathRate, rLen, IR,
                                                 interactions, pop)

print(np.average([i for i in reproduction_number if i > 0]))

# infected = sum([p.numInfected for p in pop if p.type == 'R'])
# print(infected)

plt.plot(t, S, 'b', label='S')
plt.plot(t, I, 'r', label='I')
plt.plot(t, R, 'g', label='R')
plt.plot(t, D, 'black', label='D')
# plt.fill_between(t, I, color='r')
plt.legend()
plt.title('SIR Model (default)')
plt.xlabel("Time (days)")
plt.ylabel(r"# of Persons $/10^6$")
plt.text(250, 250, "R = %.3f" % (np.average([i for i in reproduction_number if i > 0])), fontsize=10)
plt.text(250, 230, "deaths = %.0f" % (D[len(D) - 1]))
plt.show()

# plt.style.use('classic')
# fig, ax = plt.subplots()
# ax.plot(t, S, label='S')
# ax.plot(t, I, label='I')
# ax.plot(t, R, label='R')
# ax.axis('time(days)')
# leg = ax.legend()
# plt.show()
