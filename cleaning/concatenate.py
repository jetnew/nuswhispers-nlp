import pandas as pd

df = []

for i in range(627, 517, -1):
    df.append(pd.read_csv('../data/collection' + str(i) + '.csv'))


df = pd.concat(df, ignore_index=True)

df.to_csv("../data/combined.csv")