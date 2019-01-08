import pandas as pd
from random import sample,randint,uniform
import datetime
from initialization_scripts import utils
df1 = pd.read_csv('../static/datasets/created/ticket_category.csv')
df2 = pd.read_csv('../static/datasets/created/artist.csv')
df3 = pd.read_csv('../static/datasets/created/location.csv')
df4 = pd.read_csv('../static/datasets/show names.csv')
optional_capacity = [250,500,750]
optional_capacityLen = len(optional_capacity)
prizes = [50,75,100,125,150,175,200,225,250,275,300,350,375,400]
prizesLen = len(prizes)
time = [" 16:00:00"," 17:00:00"," 18:00:00", " 19:00:00", " 20:00:00", " 21:00:00"," 22:00:00", " 23:00:00",
        " 00:00:00"," 01:00:00"," 02:00:00", " 03:00:00"]
timeLen = len(time)
categories = list(df1["name"])
optionalNames = list(df4["name"])

df1Len = len(df1)
df2Len = len(df2)
df3Len = len(df3)
df4Len = len(df4)

concert_df = pd.DataFrame(columns=['id','name','location','start','end','capacity','tickets_left'])
artist_concert_df = pd.DataFrame(columns=['concert_id','artist_id'])
concert_ticket_df = pd.DataFrame(columns=['concert_id','category_id','price'])

todayDate = datetime.datetime.now()
date_time = sample([str(datetime.date(2018,11,1) + datetime.timedelta(days=x)) for x in range(0, 100)], 100)
date_timeLen = len(date_time)
concert_artist_index = 1
concert_ticket_index = 1
for i in range(1, 500):
    showsName = ""
    artists = []
    artistNum = uniform(0, 1)
    if(artistNum < 0.7):
        randArtist = randint(1,df2Len-1)
        artists.append(df2.values[randArtist][2]) #???
        showsName = optionalNames[randint(1,df4Len-1)] + " with " + df2.values[randArtist][0]
    if(artistNum >= 0.7):
        randArtist = randint(1, df2Len - 1)
        artists.append(df2.values[randArtist][2])  # ???
        showsName +=df2.values[randArtist][0] + " and "
        randArtist = randint(1, df2Len - 1)
        artists.append(df2.values[randArtist][2])  # ???
        showsName += df2.values[randArtist][0]

    for art in artists:
        artist_concert_df.loc[concert_artist_index] = [i,art]
        concert_artist_index +=1

    prize = prizes[randint(1,prizesLen-1)]
    idx = 1
    for category in categories:
        concert_ticket_df.loc[concert_ticket_index] = [i,idx,prize]
        concert_ticket_index += 1
        idx+=1
        prize += prizes[randint(1,prizesLen-1)]
    date = date_time[randint(1, date_timeLen - 1)]
    st = randint(1,timeLen/2)
    start = date
    start += time[st]
    st = randint(timeLen / 2,timeLen-1)
    end = date
    end +=time[st]
    location = df3.values[randint(1, df3Len - 1)][0]
    left = randint(0,100)
    capacity = optional_capacity[randint(0,optional_capacityLen-1)]
    concert_df.loc[i] = [i,showsName,location, start, end,capacity,left]
concert_df.to_csv("../static/datasets/created/concert.csv",sep=",",header=True, index=False)
artist_concert_df.to_csv("../static/datasets/created/artist_concert.csv",sep=",",header=True, index=False)
concert_ticket_df.to_csv("../static/datasets/created/concert_ticket.csv",sep=",",header=True, index=False)


print("done")
#for i in range(1, 3000):

'''
for i in range(0, 30):
    artist_id += sample(list(df2.artist_id), len(list(df2.artist_id)))

# Create Datetime column
for i in range(0, 3000):
    date_time += sample([str(datetime.date(2017,2,3) + datetime.timedelta(days=x)) for x in range(0, 1000)], 1000)
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

'''