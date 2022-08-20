
import dataset
import random
import decimal
import pandas as pd
import math


def filter_by_duration(keyword, dataset):
    if keyword == "very_short":
        dataset = dataset[(dataset['duration'] > 0.09375) & (dataset['duration'] <= 0.25)]
        return dataset, random.randrange(45, 120)/480
    elif keyword == "short":
        dataset = dataset[(dataset['duration'] > 0.25) & (dataset['duration'] <= 0.375)]
        return dataset, random.randrange(120, 180)/480
    elif keyword == "idk" or keyword == "":
        dataset = dataset[(dataset['duration'] > 0.09375) & (dataset['duration'] <= 1)]
        return dataset, random.randrange(45, 480)/480
    elif keyword == "long":
        dataset = dataset[(dataset['duration'] > 0.5) & (dataset['duration'] <= 0.75)]
        return dataset, random.randrange(240, 360)/480
    elif keyword == "very_long":
        dataset = dataset[(dataset['duration'] > 0.75) & (dataset['duration'] <= 1)]
        return dataset, random.randrange(360, 480)/480

def filter_by_tempo(keyword, dataset):
    if keyword == "very_slow":
        dataset = dataset[(dataset['tempo'] > 0.125) & (dataset['tempo'] <= 0.3833)]
        return dataset, random.randrange(30, 92)/240
    elif keyword == "slow":
        dataset = dataset[(dataset['tempo'] > 0.3875) & (dataset['tempo'] <= 0.483333)]
        return dataset, random.randrange(93, 116)/240
    elif keyword == "idk":
        dataset = dataset[(dataset['tempo'] > 0.3875) & (dataset['tempo'] <= .5833)]
        return dataset, random.randrange(93, 140)/240
    elif keyword == "":
        return dataset, random.randrange(30,240)/240
    elif keyword == "fast":
        dataset = dataset[(dataset['tempo'] > 0.4833) & (dataset['tempo'] <= 0.5833)]
        return dataset, random.randrange(116, 140)/240
    elif keyword == "very_fast":
        dataset = dataset[(dataset['tempo'] > 0.5875) & (dataset['tempo'] <= 1)]
        return dataset, random.randrange(141, 240)/240

def filter_by_composition(keyword,dataset):
    if keyword == "pure_vocals":
        dataset = dataset[dataset['speechiness'] > 0.15]
        return dataset, random.randrange(15, 100)/100, 0
    elif keyword == "pure_instrumental":
        dataset = dataset[dataset['instrumentalness'] > 0.72]
        return dataset, 0, random.randrange(72, 100)/100
    elif keyword == "idk":
        dataset = dataset[(dataset['speechiness'] <= 0.15) & (dataset['instrumentalness'] <= 0.72)]
        return dataset, random.randrange(2, 15)/100, random.randrange(0, 72)/100
    elif keyword == "":
        return dataset, random.randrange(0,100)/100, random.randrange(0,100)/100

def filter_by_acoustics(keyword, dataset):
    if keyword == "pure_electrical":
        dataset = dataset[dataset['acousticness'] <= 0.036200]
        return dataset, random.randrange(0, 4)/100
    elif keyword == "pure_acoustic":
        dataset = dataset[dataset['acousticness'] > 0.697000]
        return dataset, random.randrange(70, 100)/100
    elif keyword == "idk":
        dataset = dataset[(dataset['acousticness'] > 0.036200) & (dataset['acousticness'] <= 0.697000)]
        return dataset, random.randrange(4, 70)/100
    elif keyword == "":
        return dataset, random.randrange(0,100)/100

def filter_by_energy(keyword, dataset):
    if keyword == "mellow":
        dataset = dataset[(dataset['energy'] < 0.358)]
        return dataset, random.randrange(0, 36)/100
    elif keyword == "slightly_mellow":
        dataset = dataset[(dataset['energy'] >= 0.358) & (dataset['energy'] < 0.60)]
        return dataset, random.randrange(36, 60)/100
    elif keyword == "idk":
        dataset = dataset[(dataset['energy'] >= 0.358) & (dataset['energy'] < 0.784)]
        return dataset, random.randrange(36, 79)/100
    elif keyword == "":
        return dataset, random.randrange(0,100)/100
    elif keyword == "somewhat_lively":
        dataset = dataset[(dataset['energy'] >= 0.60) & (dataset['energy'] < 0.784)]
        return dataset, random.randrange(60, 79)/100
    elif keyword == "lively":
        dataset = dataset[(dataset['energy'] >= 0.784) & (dataset['energy'] <= 1)]
        return dataset, random.randrange(79, 100)/100

def filter_by_mood(keyword, dataset):
    if keyword == "somber":
        dataset = dataset[dataset['valence'] <= 0.2]
        return dataset, random.randrange(0, 20)/100
    elif keyword == "uplifting":
        dataset = dataset[dataset['valence'] >= 0.8]
        return dataset, random.randrange(80, 100)/100
    elif keyword == "idk":
        dataset = dataset[(dataset['valence'] > 0.2) & (dataset['valence'] < 0.8)]
        return dataset, random.randrange(20, 80)/100
    elif keyword == "":
        return dataset, random.randrange(0,100)/100




