
import numpy as np
import os
import pandas as pd
import random


DIR, FILENAME = os.path.split(__file__)


def normal_sample(n, mu, sigma):
    return sigma * np.random.randn(n) + mu


animals = pd.DataFrame()

weights = {"Dog": 50, "Cat": 20, "Snake": 10, "Fish": 5, "Hamster": 0.5}
legs = {"Dog": 4, "Cat": 4, "Snake": 0, "Fish": 0, "Hamster": 4}
ages = {"Dog": 18, "Cat": 20, "Snake": 15, "Fish": 10, "Hamster": 3}

fp = os.path.join(DIR, "Dog_Names.csv")
names = pd.read_csv(fp)

for a in ["Dog", "Cat", "Snake", "Fish", "Hamster"]:
    n = random.randint(100, 500)
    sigma = random.randint(1, 50) / 100
    a_w = normal_sample(n, weights[a], weights[a] * sigma)
    a_w = [abs(w) for w in a_w]
    sigma = random.randint(1, 5) / 100
    a_a = normal_sample(n, ages[a], weights[a] * sigma)
    a_a = [abs(int(a)) for a in a_a]
    df = pd.DataFrame(data={"Animal": a, "Weight": a_w, "Legs": legs[a], "Age": a_a})
    animals = animals.append(df)

animals["Name"] = [random.choice(names["DogName"]) for _ in range(len(animals))]
animals.reset_index(inplace=True, drop=True)

path = os.path.join(DIR, "animals.csv")
animals.to_csv(path, encoding="utf-8", index=False)