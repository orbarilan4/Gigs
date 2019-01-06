import pandas as pd
from random import sample,randint
import datetime
from initialization_scripts import utils

df1 = pd.read_csv('../static/datasets/places.csv')
df2 = pd.read_csv('../static/datasets/created/artist.csv')
df3 = pd.read_csv('../static/datasets/created/city.csv')

artist_id, city, date_time, price, age_limit, capacity = [], [], [], [], [], []
time = [" 16:00:00"," 17:00:00"," 18:00:00", " 19:00:00", " 20:00:00", " 21:00:00"," 22:00:00", " 23:00:00",
        " 00:00:00"," 01:00:00"," 02:00:00", " 03:00:00"]

for i in range(0, 30):
    artist_id += sample(list(df2.artist_id), len(list(df2.artist_id)))

# Create Datetime column
for i in range(0, 3000):
    date_time += sample([str(datetime.date(2019,2,3) + datetime.timedelta(days=x)) for x in range(0, 1000)], 1000)
for i in range(0, len(date_time)):
    date_time[i] += time[(randint(0, 11))]

# Create City
for i in range(0, 50):
    city += list(df1.city)
# Create Price column
for i in range(0, 20000):
    price += sample(list(range(15, 65)), 50)

# Create Age column
for i in range(0, 85000):
    age_limit += sample(list(range(18, 30)), 12)

# Create Capacity column
for i in range(0, 1200):
    capacity += sample(list(range(150, 1000)), 850)

df = pd.DataFrame(data={'artist_id': artist_id,
                        'city_id': utils.names_to_ids(city)[:len(artist_id)],
                        'date_time': date_time[:len(artist_id)],
                        'price': price[:len(artist_id)],
                        'age_limit':age_limit[:len(artist_id)],
                        'capacity':capacity[:len(artist_id)]})\
                        .drop_duplicates(subset=('artist_id','date_time'),keep='first')
df.to_csv("../static/datasets/created/concert1.csv",sep=",",header=True, index=False)