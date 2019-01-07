import pandas as pd
import random

df1 = pd.read_csv('../static/datasets/created/concert.csv')
df2 = pd.read_csv('../static/datasets/created/users.csv')

users = list(df2["id"])
concerts = list(df1['id'])
concert_capacity = list(df1["capacity"])
userLen = len(users)
concertLen = len(concerts)

df = pd.DataFrame(columns=['user_id', 'like' ,'quantity','concert_id'])
optional_capacity = [250,500,750]
capacityLen = len(optional_capacity)

index = 0

for concert in concerts:
    capacity = optional_capacity[random.randint(0,capacityLen-1)]
    participants = capacity - concert_capacity[concert-1]
    random.shuffle(users)
    idx = 0
    while(participants > 0):

        isBuy = random.uniform(0,1)
        if(isBuy <= 0.5):
            rand_ticket =random.uniform(0,1)
            if(rand_ticket <= 0.5):
                num_ticket = 1
            if (rand_ticket > 0.5 and rand_ticket <= 0.65):
                num_ticket = 2
            if (rand_ticket > 0.65 and rand_ticket <= 0.75):
                num_ticket = 3
            if (rand_ticket > 0.75 and rand_ticket <= 0.85):
                num_ticket = 4
            if (rand_ticket > 0.85 and rand_ticket <= 0.95):
                num_ticket = 5
            if (rand_ticket > 0.95):
                num_ticket = 6

            like = 1 if random.uniform(0,1) > 0.5 else 0

            df.loc[index] = [users[idx],like, num_ticket,concert]
            index+=1
            participants -=num_ticket
            idx +=1

            if(idx >= userLen):
                idx = 0
df.to_csv("../static/datasets/created/user_concert.csv",sep=",",header=True, index=False)
print("done")

