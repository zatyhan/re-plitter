import pandas as pd

df= pd.DataFrame({'name': ["zaty", "mark"], "score":[[], []]})


df.loc[df['name']=='zaty', 'score'].item().append(20)
df.loc[df['name']=='zaty', 'score'].item().append(3)
print(df)