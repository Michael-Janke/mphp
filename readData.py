import pandas as pd
import datetime

start = datetime.datetime.now()
filenameData = "TCGA-GBM-Data.csv"
filenameMetaData = "TCGA-GBM-MetaData.csv"

df = pd.DataFrame()
for chunk in pd.read_csv("data/subsets/"+filenameData, chunksize=10**3):
    df = pd.concat([df, chunk], ignore_index=True)

print(df.shape)
data = df.values

df = pd.DataFrame()
for chunk in pd.read_csv("data/subsets/"+filenameMetaData, chunksize=10**3):
    df = pd.concat([df, chunk], ignore_index=True)

print(df.shape)
metaData = df.values


print("Time elapsed: "+str(datetime.datetime.now()-start))