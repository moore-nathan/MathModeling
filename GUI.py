from tkinter import *
from PIL import ImageTk, Image
from Final import *
import requests
import json
import pandas as pd

def grabData():
    # reponse = requests.get("https://covidtracking.com/api/v1/states/current.json")
    # print(reponse.status_code)
    # print(reponse.json())
    #
    # with open('data.json', 'w') as f:
    #     json.dump(reponse.json(), f, indent=4)
    try:
        with open('data.json') as f:
            df = pd.DataFrame(json.load(f))
    except FileNotFoundError:
        reponse = requests.get("https://covidtracking.com/api/v1/states/current.json")
        with open('data.json', 'w') as f:
            json.dump(reponse.json(), f, indent=4)
        with open('data.json') as f:
            df = pd.DataFrame(json.load(f))

    return df
    # state_data = json.dumps(reponse.json(), sort_keys=False)
    # print(state_data)
    # df.to_csv("C:/Users/SFU/PycharmProjects/MathModeling/state_data.csv")
    # print(df)


df = grabData()

root = Tk()
root.title("Covid-19 Model")
root.iconbitmap("Images/SFU.ico")
# root.geometry("400x400")

def default():
    IR_entry.delete(0, END)
    interactions_entry.delete(0, END)
    rLen_entry.delete(0, END)
    deathRate_entry.delete(0, END)

    IR_entry.insert(0, IR)
    interactions_entry.insert(0, interactions)
    rLen_entry.insert(0, rLen)
    deathRate_entry.insert(0, dailyDeathRate)

def insert():
    IR_entry.delete(0, END)
    # interactions_entry.delete(0, END)
    # rLen_entry.delete(0, END)
    deathRate_entry.delete(0, END)
    print(clicked.get())
    s = df.loc[df['state'] == clicked.get()].to_dict('list')
    print(s['death'][0])
    IR_entry.insert(0, s['positive'][0] / s['totalTestResults'][0])
    deathRate_entry.insert(0, s['death'][0] / s['totalTestResults'][0])


def plot(S, I, R, D, reproduction_number, dailyDeathRate, rLen, IR, interactions, pop):
    S, I, R, D, reproduction_number, pop = SIR_Model(S.copy(), I.copy(), R.copy(), D.copy(),
                                                     reproduction_number.copy(), dailyDeathRate, rLen,
                                                     IR, interactions, pop.copy())
    # print(S)
    plt.close()
    plt.plot(t, S, 'b', label='S')
    plt.plot(t, I, 'r', label='I')
    plt.plot(t, R, 'g', label='R')
    plt.plot(t, D, 'black', label='D')
    # plt.fill_between(t, I, color='r')
    plt.legend()
    plt.title("SIRD Model")
    plt.xlabel("Time (days)")
    plt.ylabel(r"Population ($10^6$ Persons)")
    plt.text(250, 250, "R = %.3f" % (np.average([k for k in reproduction_number if k > 0])), fontsize=10)
    plt.text(250, 230, "deaths = %.0f" % (D[len(D) - 1]))
    plt.show()


IR_entry = Entry(root, width=10)
interactions_entry = Entry(root, width=10)
rLen_entry = Entry(root, width=10)
deathRate_entry = Entry(root, width=10)

IR_label = Label(root, text="Infection rate")
interactions_label = Label(root, text="Interactions")
rLen_label = Label(root, text="Disease length(days)")
deathRate_label = Label(root, text="Death Rate")

IR_entry.insert(0, IR)
interactions_entry.insert(0, interactions)
rLen_entry.insert(0, rLen)
deathRate_entry.insert(0, dailyDeathRate)

IR_label.grid(row=1, column=0, padx=10)
IR_entry.grid(row=2, column=0, padx=10)
interactions_label.grid(row=1, column=1, padx=10)
interactions_entry.grid(row=2, column=1, padx=10)
rLen_label.grid(row=1, column=2, padx=10)
rLen_entry.grid(row=2, column=2, padx=10)
deathRate_label.grid(row=1, column=3, padx=10)
deathRate_entry.grid(row=2, column=3, padx=10)

clicked = StringVar()
clicked.set(df.state[0])
#
state_drop = OptionMenu(root, clicked, *df.state)
state_drop.grid(row=3, column=0, pady=10)

state_btn = Button(root, text="Insert State Data", command=insert)
state_btn.grid(row=3, column=1)

default_btn = Button(root, text="Default (Total US)", command=default)
default_btn.grid(row=3, column=2)

plotter = Button(root, text="Plot", command=lambda: plot(S.copy(), I.copy(), R.copy(), D.copy(),
                                                         reproduction_number.copy(), float(deathRate_entry.get()), int(rLen_entry.get()),
                                                         float(IR_entry.get()), int(interactions_entry.get()), pop.copy()))
plotter.grid(row=3, column=3, sticky="SE", pady=20)

# this keeps columns spaced correctly when screen is scaled
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

root.mainloop()
