import pandas as pd
import random
from initialization_scripts import utils
from collections import defaultdict

df1 = pd.read_csv('../static/datasets/cultural-centers-theaters-historic-sites-and-galleries-location-and-contact-information.csv').fillna("Mainstream")
df2 = pd.read_csv('../static/datasets/parks.csv').fillna("Mainstream")

df3 = pd.read_csv('../static/datasets/created/city.csv')
placesLen = len(df3)


locationList = list(df2["Park Name"]) + list(df1["CENTER NAME"])

locationLen = len(locationList)

df = pd.DataFrame(columns=['id','name','city_id'])

for i in range(1,5000):
    currLocation = locationList[random.randint(1,locationLen-1)]
    currCity = df3.values[random.randint(1,placesLen-1)][2]
    df.loc[i] = [ i, currLocation, currCity]
   # df.append({'id': i, 'name': currLocation, 'city_id': currCity}, ignore_index=True)
df.to_csv("../static/datasets/created/location.csv",sep=",",header=True, index=False)


df2 = pd.DataFrame(columns=['id','name'])
df2.loc[1] = [1, 'Cheapest']
df2.loc[2] = [2, 'Golden Ring']
df2.loc[3] = [3, 'VIP']

df2.to_csv("../static/datasets/created/ticket_category.csv",sep=",",header=True, index=False)
print("done")

