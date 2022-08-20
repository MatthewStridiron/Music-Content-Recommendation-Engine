#Based on https://www.kaggle.com/code/pouyaaskari/spotify-data-analysis-project

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_track=pd.read_csv("C:/Users/mstrid/Documents/Website/SpotifyFeatures.csv")

df_track = df_track[df_track['genre'] != 'Comedy']
df_track = df_track[df_track['genre'] != "Children's Music"]
df_track = df_track[df_track['genre'] != 'Movie']

df_track=df_track[df_track['speechiness'] < 0.889] #everything above this value is speeches/audio book recordings/not songs

df_track["duration"]=df_track["duration_ms"].apply(lambda x:round(x/(1000))) #converts ms to s
df_track.drop("duration_ms",inplace=True,axis=1) #drop the ms axis.

df_track.drop(df_track[df_track['duration'] > 480].index, inplace = True)
df_track.drop(df_track[df_track['duration'] < 45].index, inplace = True)
#any entry that is longer than 8 minutes probably isn't a song. 
#any entry that isn't at least 45 seconds is probably a youtube short

#normalizing columns
df_track["duration"]=df_track["duration"].apply(lambda x:(x/(480))) #normalizes
#df_track["popularity"] = df_track["popularity"].apply(lambda x:(x/(100))) #normalizes so that data is between 0 and 1
df_track["tempo"] = df_track["tempo"].apply(lambda x:(x/(239.848))) #normalizes so that data is between 0 and 1
#239.848 is the max value in the tempo column

#dropping unnecessary columns
df_track.drop("time_signature",inplace=True,axis=1)
df_track.drop("mode",inplace=True,axis=1)
df_track.drop("key",inplace=True,axis=1)
df_track.drop("popularity",inplace=True,axis=1) #popularity should have nothing to do with music recommenders

#drops rows with the same songs
df_track = df_track.drop_duplicates(subset=['track_name','artist_name'], keep='first')

#converting decibel reading to a 0 to 100 scale
#https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
old_min = -52.457 #min loudness in db
old_max = 1.585 #max loudness in db
new_min = 0
new_max = 1

df_track["loudness"] = df_track["loudness"].apply(lambda old_value:( ( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min  )   )

track_name_lower = df_track["track_name"].str.lower()
df_track["track_name_lower"] = track_name_lower