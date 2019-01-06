import pandas as pd
from initialization_scripts import utils
from collections import defaultdict

import numpy as np

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #print (matrix)
    return (matrix[size_x - 1, size_y - 1])
levenshtein("beyonsa-low", "beyonsa")

def checkSimilaruty(artistArr):
    for artist2 in artistDic.keys():
        if (len(artistArr) > 1):
            for artist1 in artistArr:
                result = levenshtein(artist1, artist2)
                result = 1 - result / (len(artist1) + len(artist2))
                if (result >= 0.75):
                    return True
        else:
            artist1 = artistArr[0]
            result = levenshtein(artist1, artist2)
            result = 1 - result / (len(artist1) + len(artist2))
            if (result >= 0.75):
                return True
    return False


df1 = pd.read_csv('../static/datasets/10000-MTV-Music-Artists-page-1.csv').fillna("Mainstream")
df2 = pd.read_csv('../static/datasets/10000-MTV-Music-Artists-page-2.csv').fillna("Mainstream")
df3 = pd.read_csv('../static/datasets/10000-MTV-Music-Artists-page-3.csv').fillna("Mainstream")
df4 = pd.read_csv('../static/datasets/10000-MTV-Music-Artists-page-4.csv').fillna("Mainstream")
df5 = pd.read_csv('../static/datasets/metal_bands_2017.csv', encoding="ISO-8859-1")
df6 = pd.read_csv('../static/datasets/ECM_releases.csv', encoding="ISO-8859-1")
df7 = pd.read_csv('../static/datasets/MetroLyrics.csv', encoding="ISO-8859-1")


artistDic = defaultdict(int)

artist_list = list(df1.name) + list(df2.name) + list(df3.name) +\
                list(df4.name)# + list(pd.Series(df6.musician_name).unique()) +\
                #list(pd.Series(df5.band_name).unique()) + list(df7.artist)

artistDic = {i: 1 for i in artist_list}
print(len(artist_list))
for artist in list(pd.Series(df7.artist).unique()):
    artistArr = artist.replace("-"," ").split(" ")
    similarity = checkSimilaruty(artistArr)
    if(similarity == False):
        artist_list.append(artist)

artistDic = {i: 1 for i in artist_list}
print(len(artist_list))
for artist in list(pd.Series(df5.band_name).unique()):
    artistArr = artist.replace("-"," ").split(" ")
    similarity = checkSimilaruty(artistArr)
    if(similarity == False):
        artist_list.append(artist)

artistDic = {i:1 for i in artist_list}
for artist in list(pd.Series(df6.musician_name).unique()):
    artistArr = artist.replace("-"," ").split(" ")
    similarity = checkSimilaruty(artistArr)
    if(similarity == False):
        artist_list.append(artist)

print(len(artist_list))
genre_list = list(df1.genre) + list(df2.genre) + list(df3.genre) +\
               list(df4.genre) + list(map(lambda x: "Jazz",range(len(pd.Series(df6.musician_name).unique())))) + \
               list(map(lambda x: "Metal", range(len(pd.Series(df5.band_name).unique())))) +\
               list(df7.genre)

# Cleaning and fixing artist and genre data
for i in range(len(artist_list)):
    artist_list[i] = str(artist_list[i]).replace("-"," ").title()
    if str(artist_list[i]).startswith(" "):
        artist_list[i] = artist_list[i][1:]
    genre_list[i] = str(genre_list[i]).replace("Not Available", "Other").title()

# The first 3843 artists got white space at the end of there names
for i in range(len(df1.name)+len(df2.name)+len(df3.name)+len(df4.name)):
    artist_list[i] = artist_list[i][:-1]

genre_id = utils.names_to_ids(genre_list)

# Creating artist and genre dataframes
artist_df = pd.DataFrame(data={'artist_name': artist_list, 'genre_id': genre_id}).\
            drop_duplicates(subset='artist_name',keep='first')
artist_df = artist_df.assign(artist_id=list(range(len(artist_df))))  # Add artist_id column
artist_df.to_csv("../static/datasets/created/artist.csv",sep=",",header=True, index=False)

genre_df = pd.DataFrame(data={'genre_name': genre_list, 'genre_id': genre_id}).\
            drop_duplicates(subset='genre_name',keep='first')
genre_df.to_csv("../static/datasets/created/genre.csv",sep=",",header=True, index=False)




