import pandas as pd

df = pd.read_csv("mtl.csv")
df = df.head()
X = df.drop(df['Disease'], axis=1)
y = df['Disease']

from sklearn.preprocessing import LabelEncoder
lr = LabelEncoder()
y = lr.fit_transform('Disease')





