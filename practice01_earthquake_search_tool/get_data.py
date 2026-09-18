import pandas as pd
import requests
import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

#Get
apikey=os.getenv('apikey')
dataid='E-A0015-002'
format='JSON'
url=f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/{dataid}?Authorization={apikey}&format={format}'
response = requests.get(url,verify=False)
if response.status_code == 200:
    response_json = response.json()
else:
    print('error')
    print(response.text)

#Transform
dfstep1=pd.json_normalize(response_json['records']['Earthquake'])
dfstep1_ex=dfstep1.explode('Intensity.ShakingArea').reset_index(drop=True)
dfstep1_ex_detail=pd.json_normalize(dfstep1_ex['Intensity.ShakingArea']).reset_index(drop=True)
dfstep2=pd.concat([dfstep1_ex,dfstep1_ex_detail],axis=1)
dfstep2.drop(columns=['ReportType','Intensity.ShakingArea','EqStation'],inplace=True)
dfstep2.rename(columns={
    'EarthquakeInfo.OriginTime':'OriginTime',
    'EarthquakeInfo.Source':'Source',
    'EarthquakeInfo.FocalDepth':'FocalDepth',
    'EarthquakeInfo.Epicenter.Location':'Epicenter.Location',
    'EarthquakeInfo.Epicenter.EpicenterLatitude':'EpicenterLatitude',
    'EarthquakeInfo.Epicenter.EpicenterLongitude':'EpicenterLongitude',
    'EarthquakeInfo.EarthquakeMagnitude.MagnitudeValue':'MagnitudeValue',
    'EarthquakeInfo.EarthquakeMagnitude.MagnitudeType':'MagnitudeType'
    },inplace=True
)
earthquake_dict=dfstep2.to_dict(orient='records')

#Insert
mongourl=os.getenv('mongourl')
cluster=pymongo.MongoClient(mongourl)
coll=cluster['tw_earthquake_db']['tw_earthquake_coll']
coll.delete_many({})
coll.insert_many(earthquake_dict)

