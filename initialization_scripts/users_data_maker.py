import pandas as pd
import random

df2 = pd.read_csv('../static/datasets/NationalNames.csv')

user_df = pd.DataFrame(columns=['id','username', 'password','isAdmin'])

names = list(set(list(df2["Name"])))
namesDic = dict.fromkeys(names, 0)
nameLen = len(names)
for i in range(1, 20000):
    num = random.randint(1,nameLen-1)
    name = names[num]
    username = name
    if(namesDic[name] > 0):
        username = username + str(namesDic[name])
    namesDic[name] +=1

    user_df.loc[i] = [i, username, '123456', 0]
user_df.to_csv("../static/datasets/created/users.csv",sep=",",header=True, index=False)
print('done')

