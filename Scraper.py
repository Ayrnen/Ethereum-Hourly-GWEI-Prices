import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import datetime

def gasGetter():
#foundation
    import json
    import pandas as pd
    trackedValues=['safeLow','average','fast','fastest']
    df3=pd.read_csv(r'C:\Users\Aymen\Desktop\Current Shit\GasGotExtra.csv')

#webscrape
    webP=requests.get('https://ethgasstation.info/api/ethgasAPI.json')
    content=webP.content
    soup=BeautifulSoup(content, features= 'html.parser')
    json=json.loads(soup.text)

#gas values
    df1=pd.DataFrame.from_dict(json)
    df1=df1.reset_index(drop=True)
    df2=pd.DataFrame()
    for q in trackedValues:
        df2[str(q)]=df1[str(q)].apply(lambda x: x/10)

    df3['datetime']=df3['datetime'].astype('datetime64[ns]')

#datetime
    dt=pd.DataFrame()
    dt['datetime']=[datetime.datetime.utcnow()]

#merge
    df = dt.merge(df2, left_index=True, right_index=True, how='outer')
#stop index from growing infinitely
    df.reset_index()
#Drop the duplicate columns
    df.drop([col for col in df3.columns if 'drop' in col], axis=1, inplace=True)

#save and run
    df = df.drop_duplicates()
    df=df.dropna(how='any')
    print(df)
    df3=df3.append(df.iloc[0], ignore_index=True)
    df3.to_csv(r'C:\Users\Aymen\Desktop\Current Shit\GasGotExtra.csv', index=False)
    print(df3)

# Function Running every Hour
from apscheduler.schedulers.blocking import BlockingScheduler
scheduler = BlockingScheduler(timezone='utc')
scheduler.add_job(gasGetter, 'interval', hours=1)
scheduler.start()
