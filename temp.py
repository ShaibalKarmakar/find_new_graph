import pickle 
import os

with open("data.pkl", "rb") as fp:
    data = pickle.load(fp)

print(list(data.keys()))
