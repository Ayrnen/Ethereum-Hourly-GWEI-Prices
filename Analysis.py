import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import datetime
import time


#Import CSV
df=pd.read_csv('Pasta.csv')

# convert to strptime
def timed(x):
    return datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
df['datetime']=df.datetime.apply(timed)

#grab hour out of DateTime
def houred(x):
    return x.hour
df['datetime']=df.datetime.apply(houred)

#rename columns
df.rename(columns={'datetime': 'hour', 'average': 'cost'}, inplace=True)

#drop unnecessary gas values
df=df.drop(columns=['safeLow','fast','fastest'])

#barplot DataFrame
sns.barplot(data=df, x='hour', y='cost')
plt.show()


#create Easily readable Hour:Cost DataFrame
df2=pd.DataFrame()

for hour in range(24):
    df2[str(hour)]=(df.groupby('hour').get_group(1)['cost'].values).tolist()
    df2.reset_index()
print(df2)

#plot
