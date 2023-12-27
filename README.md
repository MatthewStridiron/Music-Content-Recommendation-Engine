# Music Content Recommendation Engine
made by Matthew Stridiron 

**YOUTUBE TUTORIAL (HIGHLY RECOMMENDED):** https://www.youtube.com/watch?v=n3jxHhA7N_4&ab_channel=MatthewStridiron

**REPORT:** https://www.overleaf.com/read/nrzhnhgbybdw

**WEBSITE LINK:** http://52.21.237.105/ or http://www.music-recommender.com/ from 9am-9pm EST

**About the files**
**SpotifyFeatures.zip** - the dataset
**Analysis.ipynb** - preliminary analysis on the dataset before I began work
**__init__.py** - stores all of the main functions, including the survey page's logic, the search algorithm, the registration page's logic, logging in/out, and the account recovery page's logic.
**create_table.py** - instantiates the AWS DynamoDB database that stores user music data behind the scenes
**dataset.py** - normalizing music categories, dropping unnecessary columns in the dataset that are not music-related
**filters.py** - filters music based on tempo, duration, composition, acoustics, energy, and mood
**functions.py** - separate file for generating ten recommended songs that will be returned to the user
**keys.py** - settings needed to set up AWS infrastructure
**startec2.py** - script used in AWS Lambda to automatically start the web server at 9 am EST
**stopec2.py** - script used in AWS Lambda to automatically stop the web server at 9 pm EST
