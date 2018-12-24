from flask import Flask, render_template, url_for, request, flash, redirect, session, g
import sqlite3
from forms import AdvancedSearch, RegistrationForm, LoginForm, UpdateProfileForm, AddDelConcert
import numpy as np
import json
from datetime import date, datetime
import wikipedia

import models as model

db = model.modelDB()

DATABASE = 'db/gigs.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# db_connection.mysql_db_connection()
app = Flask(__name__)
#app.config['MYSQL_DATABASE_HOST'] = '85.10.205.173'
#app.config['MYSQL_DATABASE_USER'] = 'orbari123456'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'Oliver123'
#app.config['MYSQL_DATABASE_DB'] = 'music321'
app.config['SECRET_KEY'] = 'f9bf78b9a18ce6d46a0cd2b0b86df9da'
#mysql.init_app(app)

@app.teardown_appcontext
def close_connection(exception):
    db.close_connection(exception)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/isloggedin", methods=['GET'])
def is_logged_in():
    if session:
        if session['is_admin']:
            return '2'
        elif session['logged_in']:
            return '1'

    return '0'

@app.route("/wiki_summary", methods=['GET'])
def wiki_summary():
    artist = request.args.get('artist')

    wikipage = wikipedia.page(artist)

    data = {}
    data['desc'] = wikipedia.summary(artist)
    imgs = []
    for i in wikipage.images:
        if not (i.endswith('svg') | i.endswith('png')):
            imgs.append(i)

    data['images'] = imgs
    return json.dumps(data)


# ================================
# ===== User Page Options ======
# ================================
@app.route("/show_profile", methods=['GET', 'POST'])
def show_profile():
    if session['logged_in'] is False:
        return render_template('index.html')
    return render_template('show_profile.html')

'''
@app.route("/update_profile", methods=['GET', 'POST'])
def update_profile():
    if session['logged_in']:
        form = UpdateProfileForm(request.form)
        if request.method == 'POST' and form.validate():
         
            city_record = db.getRecord(form.city.data)
            if city_record:
                city_record = city_record.pop(0)
                cur.execute("UPDATE user SET user.age = ? , user.city_id = ?, user.picture = ?  WHERE user.username = ?",
                            (form.age.data, city_record[1], form.picture.data, session['username']))
                
                session['age'] = form.age.data
                session['city_name'] = form.city.data.title()
                session['city_id'] = city_record[1]
                session['picture'] = form.picture.data
                cur.execute("SELECT city.city_name, country.country_name FROM city,country "
                            "WHERE country.country_id = city.country_id AND city.city_id = ?"
                            , session['city_id'])  # Get city and country name from user

                place = list(cur.fetchall()).pop(0)
                session['country_name'] = place[1]
                #flash(f'Your account updated!', 'success')
                return show_profile()
            elif len(city_record) == 0:
                #flash(f'The entered city does not exist!', 'error')
                return redirect(url_for('update_profile'))
    else:
        return render_template('index.html')
    return render_template('update_profile.html', form=form)

'''

@app.route("/personal_tickets", methods=['GET', 'POST'])
def personal_tickets():
    if session['logged_in'] is False:
        return home()

    records = db.getPersonalTikets(session['username'])
    return render_template('my_tickets.html', orders=False, records=records)


# ================================
# ===== Admin Options ======
# ================================
@app.route("/analytics", methods=['GET', 'POST'])
def analytics():
    if session['is_admin'] and session['logged_in']:
        form = AdvancedSearch(request.form)
        age_limit = list(range(18,30))
        session['country_input_exists'] = None
        if request.method == 'POST' and form.validate():
            cur = get_db().cursor()
            colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA", "#ABCDEF", "#DDDDDD", "#ABCABC"]
            # Checking if the entered country is exist
            cur.execute("SELECT country_name FROM country WHERE country_name = ?", form.country.data)
            country = cur.fetchall()
            if len(country) == 0:
                #flash(f'The entered country does not exist!', 'error')
                return redirect(url_for('analytics'))
            else:
                session['country_input_exists'] = form.country.data
                # Searching for top-10 host cities in selected (by user) country
                cur.execute("SELECT city.city_name,counter.job FROM city AS city, "
                            "(SELECT concert.city_id,count(*) AS 'job' FROM concert, city, country "
                            "WHERE concert.city_id = city.city_id AND city.country_id = country.country_id "
                            "AND country.country_name = COALESCE(?,country.country_name) "
                            "GROUP BY concert.city_id "
                            "ORDER BY job DESC LIMIT 10) AS counter "
                            "WHERE counter.city_id = city.city_id", form.country.data)
                freq_city = np.array(list(cur.fetchall()), dtype=np.dtype('object,int'))

                # Searching for top-10 hosted artists in selected (by user) country
                cur.execute("SELECT artist.artist_name,counter.job FROM artist AS artist, "
                            "(SELECT concert.artist_id,count(*) AS 'job' FROM concert, city, country "
                            "WHERE concert.city_id = city.city_id AND city.country_id = country.country_id "
                            "AND country.country_name = COALESCE(?,country.country_name) "
                            "GROUP BY concert.artist_id "
                            "ORDER BY job DESC LIMIT 10) AS counter "
                            "WHERE counter.artist_id = artist.artist_id", form.country.data)
                freq_artist = np.array(list(cur.fetchall()), dtype=np.dtype('object,int'))

                # Age limit distribution in selected (by user) country
                cur.execute("SELECT concert.age_limit,count(*) AS 'job' FROM concert, city, country "
                            "WHERE concert.city_id = city.city_id AND city.country_id = country.country_id "
                            "AND country.country_name = COALESCE(?,country.country_name) "
                            "GROUP BY concert.age_limit ORDER BY concert.age_limit LIMIT 12", form.country.data)
                freq_age_limit = np.array(list(cur.fetchall()), dtype=np.dtype('int,int'))

                return render_template('analytics.html', form=form,gigs_count=sum(freq_age_limit['f1']),
                                       set=[zip(freq_city['f1'], list(freq_city['f0']), colors),
                                            zip(freq_artist['f1'], list(freq_artist['f0']), colors)],
                                       values=freq_age_limit['f1'],labels=freq_age_limit['f0'])
    else:
        return render_template('index.html')
    return render_template('analytics.html',gigs_count=0,form=form, set=[], labels=[], values=[])



@app.route('/search', methods=['GET'] )
def search():
    filter = request.args.get('term', '', type=str).strip()
    artist = request.args.get('artist', '', type=str).strip()
    cur = get_db().cursor()
    if (artist == ''):
        cur.execute("SELECT city.city_id, city_name, country_name "
                    "FROM city "
                    "INNER JOIN country "
                    "ON city.country_id = country.country_id "
                    "AND city_name like ? "
                    "LIMIT 5", ('%' + filter + '%',))
    else:
        cur.execute("SELECT city.city_id, city_name, country_name "
                    "FROM city "
                    "INNER JOIN country "
                    "ON city.country_id = country.country_id "
                    "AND city_name like ? "                
                    "INNER JOIN concert "
                    "ON concert.city_id = city.city_id "
                    "INNER JOIN artist "
                    "ON concert.artist_id = artist.artist_id "
                    "AND artist_name like ? "
                    "LIMIT 5", ('%' + filter + '%','%' + artist + '%'))
    rows = cur.fetchall()

    if (artist == ''):
        cur.execute("SELECT country_id, country_name "
                    "FROM country "
                    "WHERE country_name like ? "
                    "LIMIT 5", ('%' + filter + '%',))
    else:
        cur.execute("SELECT country.country_id, country_name "
                    "FROM city "
                    "INNER JOIN country "
                    "ON city.country_id = country.country_id "
                    "AND city_name like ? "
                    "INNER JOIN concert "
                    "ON concert.city_id = city.city_id "
                    "INNER JOIN artist "
                    "ON concert.artist_id = artist.artist_id "
                    "AND artist_name like ? "
                    "LIMIT 5", ('%' + filter + '%', '%' + artist + '%',))

    rows2 = cur.fetchall()

    rowarray_list = {}
    for row in rows:
        rowarray_list[row[0]] = row[1] + ', ' + row[2]

    j = [{'id': str(k), 'label': v, 'value': v, 'category' : 'Cities'} for k, v in rowarray_list.items()]

    rowarray_list = {}
    for row in rows2:
        rowarray_list[row[0]] = row[1]

    j += [{'id': str(k), 'label': v, 'value': v, 'category': 'Countries'} for k, v in rowarray_list.items()]

    return json.dumps(j, indent=4)


@app.route('/search_artist', methods=['GET'] )
def search_artist():
    artist = request.args.get('term', '', type=str)

    rows = db.searchArtist(artist)

    rowarray_list = {}
    for row in rows:
        rowarray_list[row[0]] = row[1]

    j = [{'id': str(k), 'label': v, 'value': v} for k, v in rowarray_list.items()]

    return json.dumps(j, indent=4)

@app.route('/edit_concert', methods=['GET'] )
def edit_concert():
    if session['is_admin']:
        id = request.args.get('id', '', type=int)

        row,columns = db.getConcert(id)
        result = [{columns[index][0]: column for index, column in enumerate(row)}]

        return json.dumps(result, indent=4)

    return ''

@app.route('/add_concert', methods=['GET', 'POST'])
def add_concert():
    if session['is_admin'] is False:
        return home()

    if request.method == 'GET':
        return render_template("add_concert.html")

    name = request.form.get('name', '', type=str)
    capacity = request.form.get('capacity', '', type=int)

    cur = db.addConcert(name, capacity)

    return '0'

@app.route('/del_concert', methods=['GET'])
def del_concert():
    if session['is_admin']:
        id = request.args.get('id', -1, type=int)
        db.deleteConcert(id)
        return '0'
    return '1'

# Convert to string and if doesnt get anything return str("")
def xstr(s):
    if s is None:
        return ''
    return str(s.encode('utf-8'))[2:-1].strip()


# ================================
# ===== General Options ======
# ================================
@app.route('/find', methods=['GET', 'POST'])
def advanced_search():
    return render_template("result.html", records=[], orders=True)

@app.route('/hot_concerts', methods=['GET'])
def hot_concerts():
    records = []

    cur = get_db().cursor()

    cur.execute(
            "SELECT artist.artist_name ,concert.date_time , city.city_name, country.country_name, "
            "genre.genre_name, concert.age_limit , concert.price, concert.capacity "
            "FROM city, concert, artist, genre, country "
            "WHERE concert.city_id = city.city_id AND country.country_id = city.country_id "
            "AND concert.artist_id = artist.artist_id AND artist.genre_id = genre.genre_id "                        
            "ORDER BY concert.price LIMIT 5")

    records = cur.fetchall()
    columns = cur.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in records]
    return json.dumps(result, default=json_serial)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type ? not serializable" % type(obj))

@app.route('/find2', methods=['GET', 'POST'])
def advanced_search2():
    form = AdvancedSearch(request.form)
    records = []
    if request.method == 'POST':
        artist = form.artist.data if form.artist.data != '' else None
        city = form.city.data if form.city.data != '' else None
        country = form.country.data if form.country.data != '' else None
        date = form.date.data if form.date.data != '' else None
        genre = form.genre.data if form.genre.data != '' else None
        min_age = form.min_age.data if form.min_age.data != '' else 0
        max_age = form.max_age.data if form.max_age.data != '' else 100
        min_price = form.min_price.data if form.min_price.data != '' else 0
        max_price = form.max_price.data if form.max_price.data != '' else 100
        page = int(form.page.data) * 10 if form.page.data != '' else 0
        cur = get_db().cursor()

        cur.execute(
            "SELECT concert.name ,concert.start  "            
            "FROM concert "
            "WHERE ((concert.name LIKE COALESCE(?,concert.name)) "            
            ")",
            (("%" + xstr(artist) + "%"),))
        records = cur.fetchall()
        columns = cur.description
        result = [{columns[index][0]: column for index, column in enumerate(value)} for value in records]

    return json.dumps(result, default=json_serial)




# ================================
# ===== Users Options ======
# ================================
@app.route('/buy_tickets', methods=['GET', 'POST'])
def buy_tickets():
    if request.method == 'POST':
        for record in request.form.getlist('checks'):
            print(record)
            cur = get_db().cursor()
            # Casting
            record = get_record(record)
            # Get artist id
            cur.execute("SELECT artist.artist_name, artist.artist_id FROM artist,genre "
                        "WHERE genre.genre_id = artist.genre_id AND artist_name = ? AND genre_name = ?", (record[0], record[4]))
            artist_record = list(cur.fetchall()).pop(0)
            # Get capacity and age limit for concert
            cur.execute("SELECT capacity,age_limit FROM concert WHERE artist_id = ? AND date_time = ?",
                        (artist_record[1], record[1]))
            concert_data = list(cur.fetchall()).pop(0)

            # If there are tickets available
            if int(concert_data[0]) > 0 and int(session['age']) >= int(concert_data[1]):
                try:
                    cur.execute("INSERT INTO user_concert (username,artist_id,date_time) VALUES (?,?,?)",
                                (session['username'],artist_record[1] , record[1])) # New Add ticket to user_concert
                    cur.execute("UPDATE concert SET capacity = (capacity - 1) WHERE artist_id = ? AND date_time = ?",
                                (artist_record[1], record[1]))  # Capacity update after purchase
                    
                    #flash(f"You bought some tickets ! You can view them on your profile", 'success')
                except:
                    pass
                    #flash(f"Already have a ticket for {record[0]}'s gig on {record[1]} !", 'warning')
            elif int(concert_data[0]) == 0:
                pass
                #flash(f"No tickets available for {record[0]}'s gig on {record[1]} !", 'error')
            elif int(concert_data[1]) > int(session['age']):
                pass
                #flash(f"You are under age for {record[0]}'s gig on {record[1]} !", 'error')
    return render_template("index.html")


@app.route("/recommendations", methods=['GET', 'POST'])
def recommendations():
    if session['logged_in']:
        cur = get_db().cursor()
        # We want to get the most popular genre by the user
        # At first, We are looking for the number of tickets for each artist, Then we get there genre
        # And in the end we group the number of tickets together for each genre
        cur.execute("SELECT genre.genre_id, SUM(counter.job) as 'number_of_tickets' "
                    "FROM artist,genre, "
                    "(SELECT COUNT(user_concert.artist_id) AS 'job', user_concert.artist_id AS 'artist_id' "
                    "FROM user_concert,concert,artist "
                    "WHERE user_concert.artist_id = concert.artist_id AND user_concert.date_time = concert.date_time "
                    "AND concert.artist_id = artist.artist_id "
                    "AND user_concert.username = ? "
                    "GROUP BY concert.artist_id ORDER BY job DESC) AS counter "
                    "WHERE counter.artist_id = artist.artist_id AND artist.genre_id = genre.genre_id "
                    "GROUP BY genre.genre_id ORDER BY number_of_tickets DESC LIMIT 5"
                    , (session['username']))
        top_5_genres = [item[0] for item in list(cur.fetchall())]
        print(len(top_5_genres))
        cur.execute("SELECT genre.genre_id FROM genre")
        top_5_genres = list(cur.fetchall()) if len(top_5_genres) == 0 else top_5_genres
        # Searching for top-10 gigs base on user's country and user's age
        cur.execute("SELECT artist.artist_name, concert.date_time, city.city_name, country.country_name, "
                    "genre.genre_name, concert.age_limit, concert.price, concert.capacity "
                    "FROM city, concert, artist, genre, country "
                    "WHERE concert.city_id = city.city_id AND country.country_id = city.country_id "
                    "AND concert.artist_id = artist.artist_id AND artist.genre_id = genre.genre_id "
                    "AND city.country_id = ? AND concert.age_limit <= ? AND genre.genre_id IN ? "
                    "ORDER BY concert.price ASC LIMIT 10"
                    , (session['country_id'], session['age'],top_5_genres))
        records = cur.fetchall()
    else:
        return render_template('index.html')
    return render_template('result.html', orders=True, records=records)


# ================================
# ===== User Authentication ======
# ================================
@app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm(request.form)
    if request.method == 'POST':

        cur = get_db().cursor()

        cur.execute("INSERT INTO user (username,age,city_id,password,is_admin,picture) VALUES (?,?,?,?,?,?)",
                    (form.username.data, 0, 0, form.password.data,False,''))
        cur.connection.commit()

        cur.execute("SELECT username, city_id, age, is_admin, picture FROM user WHERE username = ? AND password = ? ",
                    (form.username.data, form.password.data))
        user = cur.fetchall()
        if len(user) != 0:
            record = list(user).pop(0)
            session['logged_in'] = True
            session['username'] = record[0]
            session['city_id'] = record[1]
            session['age'] = record[2]
            session['is_admin'] = record[3]
            session['picture'] = record[4]  # Get city and country name from user
            return '0'

        return '1'

    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':

        user = db.login(form.username.data,form.password.data)
        if len(user) != 0:
            record = list(user).pop(0)
            session['logged_in'] = True
            session['username'] = record[0]
            session['city_id'] = record[1]
            session['age'] = record[2]
            session['is_admin'] = record[3]
            session['picture'] = record[4]

            return '0'
        else:
            return '1'
    return render_template('login.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['is_admin'] = False
    return home()


if __name__ == "__main__":
    app.debug = True
    app.run()