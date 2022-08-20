
import dataset
import math

def generate_songs(duration, tempo, speechiness, instrumentalness, acoustics, energy, mood):
    top_ten_songs = []
    for row in dataset.df_track.index:
        distance = math.sqrt( (duration - dataset.df_track['duration'][row])**2 + (tempo - dataset.df_track['tempo'][row])**2 + (speechiness - dataset.df_track['speechiness'][row])**2 
                                     + (instrumentalness - dataset.df_track['instrumentalness'][row])**2 + (acoustics - dataset.df_track['acousticness'][row])**2  + (energy - dataset.df_track['energy'][row])**2 
                                     + (mood - dataset.df_track['valence'][row])**2 
                                     )
        dictionary = {'distance': distance, 'artist_name': dataset.df_track['artist_name'][row] , 'track_name': dataset.df_track['track_name'][row], 'track_id': dataset.df_track['track_id'][row] }
        
        if len(top_ten_songs) < 10:
            top_ten_songs.append(dictionary)
            top_ten_songs = sorted(top_ten_songs, key=lambda n: n['distance'])
        else:
            max_distance = top_ten_songs[-1]["distance"]
            if distance < max_distance:
                top_ten_songs.remove( top_ten_songs[-1])
                top_ten_songs.append(dictionary)
                top_ten_songs = sorted(top_ten_songs, key=lambda n: n['distance'])

    return top_ten_songs
