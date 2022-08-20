from flask import Flask, flash, redirect, render_template, request, url_for, session
from datetime import timedelta
import boto3 
import keys
import dataset
import functions
import filters
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)


dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY)

copy_of_dataset = dataset.df_track

from boto3.dynamodb.conditions import Key, Attr

@app.route("/survey",  methods=["POST","GET"])
def survey():
    if "user" in session:
        if request.method == 'POST':
            duration = request.form["select_duration"]
            tempo = request.form["select_tempo"]
            composition = request.form["select_music_composition"]
            acoustics = request.form["select_instruments"]
            energy = request.form["select_music_energy"]
            mood = request.form["select_mood"]

            dataset.df_track, duration = filters.filter_by_duration(duration, dataset.df_track)
            dataset.df_track, tempo = filters.filter_by_tempo(tempo, dataset.df_track)
            dataset.df_track, speechiness, instrumentalness = filters.filter_by_composition(composition, dataset.df_track)
            #never run into any instances where there are 0 entries in the database, so I return the database itself

            print(dataset.df_track.shape)

            temp_copy, acoustics = filters.filter_by_acoustics(acoustics, dataset.df_track)
            if(len(temp_copy) == 0):
                flash(f"Could not filter based on the music's acoustics due to your previous preference filters. Will retrieve songs that closely resemble preferences.")
            elif len(temp_copy) >= 10:
                dataset.df_track = temp_copy

            print(dataset.df_track.shape)

            temp_copy, energy = filters.filter_by_energy(energy, dataset.df_track)
 
            if(len(temp_copy) == 0):
                flash(f"Could not filter based on whether the music is lively or mellow due to your previous preference filters. Will retrieve songs that closely resemble preferences.")
            elif len(temp_copy) >= 10:
                dataset.df_track = temp_copy


            print(dataset.df_track.shape)

            temp_copy, mood = filters.filter_by_mood(mood, dataset.df_track)
            if(len(temp_copy) == 0):
                flash(f"Could not filter based on whether the music is cheerful or somber due to your previous preference filters. Will retrieve songs that closely resemble preferences.")
            elif len(temp_copy) >= 10:
                dataset.df_track = temp_copy


            print(dataset.df_track.shape)
            top_ten_songs = []

            table = dynamodb.Table('users')

            response = table.query(
                    KeyConditionExpression=Key('username').eq(session["user"])
            )
            items = response['Items']
            passwd = items[0]['password']
            user = items[0]['username']

            times_searched = int(items[0]['times_searched'])
            
            if times_searched == 0:
                top_ten_songs = functions.generate_songs(duration, tempo, speechiness, instrumentalness, acoustics, energy, mood)
            else:
                old_duration = items[0]['duration']
                old_tempo = items[0]['tempo']
                old_speechiness = items[0]['speechiness']
                old_instrumentalness = items[0]['instrumentalness']
                old_acoustics = items[0]['acousticness']
                old_energy = items[0]['energy']
                old_valence = items[0]['valence']

                old_weight = Decimal('0.25')
                new_weight = Decimal('0.75')

                print(old_duration, old_tempo, old_speechiness, old_instrumentalness, old_acoustics, old_energy, old_valence)
                print(duration, tempo, speechiness, instrumentalness, acoustics, energy, mood)

                duration = (Decimal(str(old_duration)) * old_weight) + (Decimal(str(duration)) * new_weight)
                tempo = (Decimal(str(old_tempo)) * old_weight) + (Decimal(str(tempo)) * new_weight)
                speechiness = (Decimal(str(old_speechiness)) * old_weight) + (Decimal(str(speechiness)) * new_weight)
                instrumentalness = (Decimal(str(old_instrumentalness)) * old_weight) + (Decimal(str(instrumentalness)) * new_weight)
                acoustics = (Decimal(str(old_acoustics)) * old_weight) + (Decimal(str(acoustics)) * new_weight)
                energy = (Decimal(str(old_energy)) * old_weight) + (Decimal(str(energy)) * new_weight)
                mood = (Decimal(str(old_valence)) * old_weight) + (Decimal(str(mood)) * new_weight)

                top_ten_songs = functions.generate_songs(float(duration), float(tempo), float(speechiness), float(instrumentalness), float(acoustics), float(energy), float(mood))

            print(duration, tempo, speechiness, instrumentalness, acoustics, energy, mood)

            #will be displayed in the main home page once the user logs in again.
            arr = []
            for i in range(0, len(top_ten_songs)):
                arr.append("https://open.spotify.com/track/" + str(top_ten_songs[i]["track_id"]) + "?si=3407625dfb4b413f&nd=1")
                
                   
            for i in range(0, len(top_ten_songs)):
                string = str(i+1) + ". "
                j = 0
                for key in top_ten_songs[i]:
                    if key == "track_id":
                        string = "spotify url: " + "https://open.spotify.com/track/" + str(top_ten_songs[i][key]) + "?si=3407625dfb4b413f&nd=1"
                        flash(f"{string}")
                        flash(f"--------------------------")
                    elif key != "distance":
                        if j == 0:
                            string = string + str(key) + ": " + str(top_ten_songs[i][key]) + "\t\n"
                            j=1
                        else:
                            string = str(key) + ": " + str(top_ten_songs[i][key]) + "\n"
                        flash(f"{string}")

            #save to database

            table.put_item(Item={
                            'username': user,
                            'password': passwd,
                            'songs': arr,
                            'duration': Decimal(str(duration)),
                            'tempo': Decimal(str(tempo)),
                            'speechiness': Decimal(str(speechiness)),
                            'instrumentalness': Decimal(str(instrumentalness)),
                            'acousticness': Decimal(str(acoustics)),
                            'energy': Decimal(str(energy)),
                            'valence': Decimal(str(mood)),
                            'times_searched': 1
                        })           

            flash("Music preferences saved to your account.")   

            dataset.df_track = copy_of_dataset
            return render_template('user.html')
        else:
            return render_template('survey.html')
    else:
        return redirect(url_for("index"))

@app.route("/search_song", methods=["POST","GET"])
def search_song():
    if "user" in session:
        if request.method == 'POST':
            song_name = request.form['sname']
            song_name.lower()

            found = 0

            for row in dataset.df_track.index:

                if dataset.df_track["track_name_lower"][row] == song_name.lower():
                    found = 1

                    duration = Decimal(str(dataset.df_track['duration'][row]))
                    tempo = Decimal(str(dataset.df_track['tempo'][row]))
                    speechiness = Decimal(str(dataset.df_track['speechiness'][row]))
                    instrumentalness = Decimal(str(dataset.df_track['instrumentalness'][row]))
                    acousticness = Decimal(str(dataset.df_track['acousticness'][row]))
                    energy = Decimal(str(dataset.df_track['energy'][row]))
                    valence = Decimal(str(dataset.df_track['valence'][row]))


                    table = dynamodb.Table('users')

                    response = table.query(
                                        KeyConditionExpression=Key('username').eq(session["user"])
                     )
                    items = response['Items']
                    passwd = items[0]['password']
                    user = items[0]['username']

                    times_searched = int(items[0]['times_searched'])
                    #print(times_searched, type(times_searched))

                    
                    if times_searched == 0:
                        table.put_item(Item={
                            'username': user,
                            'password': passwd,
                            'duration': duration,
                            'tempo': tempo,
                            'speechiness': speechiness,
                            'instrumentalness': instrumentalness,
                            'acousticness': acousticness,
                            'energy': energy,
                            'valence': valence,
                            'times_searched': 1
                        })   
                    else: #these are all of type decimal.Decimal
                        old_duration = items[0]['duration']
                        old_tempo = items[0]['tempo']
                        old_speechiness = items[0]['speechiness']
                        old_instrumentalness = items[0]['instrumentalness']
                        old_acoustics = items[0]['acousticness']
                        old_energy = items[0]['energy']
                        old_valence = items[0]['valence']

                        old_weight = Decimal('0.6')
                        new_weight = Decimal('0.4')

                        
                        table.put_item(Item={
                            'username': user,
                            'password': passwd,
                            'duration': Decimal(str((old_duration * old_weight) + (duration * new_weight))),
                            'tempo': Decimal(str((old_tempo * old_weight) + (tempo * new_weight))),
                            'speechiness': Decimal(str((old_speechiness * old_weight) + (speechiness * new_weight))),
                            'instrumentalness': Decimal(str((old_instrumentalness * old_weight) + (instrumentalness * new_weight))),
                            'acousticness': Decimal(str((old_acoustics * old_weight) + (acousticness * new_weight))),
                            'energy': Decimal(str((old_energy * old_weight) + (energy * new_weight))),
                            'valence': Decimal(str((old_valence * old_weight) + (valence * new_weight))),
                            'times_searched': 1
                        }) 
                        
                    


                    dictionary = {'artist_name': dataset.df_track['artist_name'][row] , 'track_name': dataset.df_track['track_name'][row], 'track_id': dataset.df_track['track_id'][row] }
                    string = ""
                    j = 0
                    for key in dictionary.keys():
                        if key == "track_id":
                            string = "spotify url: " + "https://open.spotify.com/track/" + str(dictionary[key]) + "?si=3407625dfb4b413f&nd=1"
                            flash(f"{string}")
                            flash(f"--------------------------")
                        else: 
                            if j == 0:
                                string = string + str(key) + ": " + str(dictionary[key]) + "\t\n"
                                j=1
                            else:
                                string = str(key) + ": " + str(dictionary[key]) + "\n"
                            flash(f"{string}")

                    break

            if found == 0:
                flash("Song not found")
            
            return render_template('user.html')
        else:
            return render_template('search_song.html')
    else:
        return redirect(url_for("index"))

@app.route("/register", methods=["POST","GET"])
def register():    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        table = dynamodb.Table('users')
        

        response = table.query(
                    KeyConditionExpression=Key('username').eq(username)
            )
        if response["Items"] != []:
            flash(f"Username already exists.")
        else:
            table.put_item(
                        Item={
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'times_searched' : 0,
                'duration': 0,
                'tempo': 0,
                'speechiness': 0,
                'instrumentalness': 0,
                'acousticness': 0,
                'energy': 0,
                'mood': 0,
                'valence': 0
                    }
                )

            flash("Registration Complete. Please Login to your account!")   

        return redirect(url_for("index"))

    return render_template('register.html')

@app.route("/user")
def user(): #individual user page
    if "user" in session:
        user = session["user"]
        return render_template("user.html",user=user)
    else:
        flash("You have been logged out.")
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("You have automatically been logged out.", "info")
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/recover_account", methods=["POST","GET"])
def recover_account():
    if request.method == "POST":
        user = request.form["username"]
        if(user == ""):
            flash(f"Please enter a username")
            return render_template("recover_account.html")

        table = dynamodb.Table('users')

        try:
            user = request.form["username"]
            response = table.query(
                    KeyConditionExpression=Key('username').eq(user)
            )

            items = response['Items']
            passwd = items[0]['password']

            flash(f"Password: {passwd}")
        except:
            flash(f"Username not found.")

    else:
        if "user" in session: #if user is logged in
            flash("You are already logged in!")
            return redirect(url_for("user"))

    return render_template("recover_account.html")

@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        passwd = request.form["password"]

        if(user == "" or passwd == ""):
            flash(f"Login unsuccessful. Please try again.")
            return redirect(url_for("index"))

        
        table = dynamodb.Table('users')
        try:
            response = table.query(
                    KeyConditionExpression=Key('username').eq(user)
            )

            items = response['Items']
            if passwd == items[0]['password'] and user == items[0]['username']:
                session["user"] = user
                flash(f"Welcome back {user}!")

                try:
                    songs = items[0]['songs']
                    flash(f"Here is the Spotify music generated from the last time you entered the site.")
                    flash(f"{songs}")
                except KeyError:
                    flash(f"It looks like this is your first time visiting. Click the link below to get started.")


                return redirect(url_for("user"))
            else:
                flash(f"Login unsuccessful. Please try again.")
                return redirect(url_for("index"))

        except IndexError:
            flash(f"Login unsuccessful. Please try again.")
            return redirect(url_for("index"))


    else:
        if "user" in session: #if user is logged in
            flash("You are already logged in!")
            return redirect(url_for("user"))
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

    #port = 80

