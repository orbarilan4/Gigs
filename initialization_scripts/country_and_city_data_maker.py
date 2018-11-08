import pandas as pd
from initialization_scripts import utils

df = pd.read_csv('../static/datasets/places.csv')
city_list = list(df.city)
country_list = list(df.country)

utils.names_to_ids(city_list)
utils.names_to_ids(country_list)

# Creating country and city dataframes
city_df = pd.DataFrame(data={'city_name': city_list, 'city_id': utils.names_to_ids(city_list)}).\
            drop_duplicates(subset='city_id',keep='first')
city_df.to_csv("../static/datasets/created/city.csv",sep=",",header=True, index=False)

country_df = pd.DataFrame(data={'country_name': country_list, 'country_id': utils.names_to_ids(country_list)}).\
            drop_duplicates(subset='country_id',keep='first')
country_df.to_csv("../static/datasets/created/country.csv",sep=",",header=True, index=False)
