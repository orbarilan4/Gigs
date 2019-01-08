from flask import Flask, render_template, url_for, request, flash, redirect, session, g
import time,sys
from flaskext.mysql import MySQL
from forms import AdvancedSearch, RegistrationForm, LoginForm, UpdateProfileForm, AddDelConcert
import numpy as np
import json
from datetime import date, datetime
import wikipedia

import models as model



# db_connection.mysql_db_connection()
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1q2w3e4r'
app.config['MYSQL_DATABASE_DB'] = 'music321'
app.config['SECRET_KEY'] = 'f9bf78b9a18ce6d46a0cd2b0b86df9da'
mysql.init_app(app)

db = model.modelDB(mysql)

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
                cur.execute("SELECT city.name, country.country.name FROM city,country "
                            "WHERE country.id = city.country_id AND city.id = ?"
                            , session['city_id'])  # Get city and country name from user

                place = list(cur.fetchall()).pop(0)
                session['country.name'] = place[1]
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

    records = db.getPersonalTikets(session['user_id'])
    return render_template('my_tickets.html', orders=False, records=records)


# ================================
# ===== Admin Options ======
# ================================
def get_db():
    return mysql.connect()


@app.route("/analytics", methods=['GET', 'POST'])
def analytics():
    if session['is_admin'] and session['logged_in']:
        form = AdvancedSearch(request.form)
        age_limit = list(range(18,30))
        session['country_input_exists'] = None
        artist_and_concert_percent_list = None

        number_concerts_per_artist = db.analytics_get_concert_number_per_artist()
        number_concerts_per_genre = db.analytics_get_concert_number_per_genre()
        analytics_get_concert_number_per_genre_per_month = db.analytics_get_concert_number_per_genre_per_month()
        analytics_get_capacity_percent_per_artist = db.analytics_get_capacity_percent_per_artist()
        analytics_get_capacity_percent_per_concert_per_artist = db.analytics_get_capacity_percent_per_concert_per_artist()
        artist_and_concert_percent_list = dict()

        for item in analytics_get_capacity_percent_per_concert_per_artist:
            # artist_concerts = dict()
            artist_concerts = dict()
            artist_concerts.update({item[2]: item[5]})
            if item[0] in artist_and_concert_percent_list:
                artist_and_concert_percent_list[item[0]].update(artist_concerts)
            else:
                artist_and_concert_percent_list.update({item[0]: artist_concerts})
        artist_and_concert_percent_list2 = dict()
        for the_key, the_value in artist_and_concert_percent_list.items():
            if the_value.items().__len__()>1:
                artist_and_concert_percent_list2.update({the_key:the_value})
        return render_template('analytics.html', form=form, gigs_count=0,
                               number_concerts=number_concerts_per_artist,
                               number_concerts_per_genre=number_concerts_per_genre,
                               analytics_get_concert_number_per_genre_per_month=analytics_get_concert_number_per_genre_per_month,
                               analytics_get_capacity_percent_per_artist=analytics_get_capacity_percent_per_artist,
                               analytics_get_capacity_percent_per_concert_per_artist=analytics_get_capacity_percent_per_concert_per_artist,
                               artist_and_concert_percent_list = artist_and_concert_percent_list2)
    else:
        return render_template('index.html')




@app.route('/search', methods=['GET'] )
def search():
    filter = request.args.get('term', '', type=str).strip()
    artist = request.args.get('artist', '', type=str).strip()
    cur = get_db().cursor()
    if (artist == ''):
        rowsCities=db.selectCities(filter)

    else:
        rowsCities = db.selectCitiesArtists(filter,artist)


    if (artist == ''):
        rowsCountries = db.selectCountries(filter)

    else:
        rowsCountries = db.selectCountriesArtists(filter,artist)


    rowarray_list = {}
    for row in rowsCities:
        rowarray_list[row[0]] = row[1] + ', ' + row[2]

    j = [{'id': str(k), 'label': v, 'value': v, 'category' : 'Cities'} for k, v in rowarray_list.items()]

    rowarray_list = {}
    for row in rowsCountries:
        rowarray_list[row[0]] = row[1]

    j += [{'id': str(k), 'label': v, 'value': v, 'category': 'Countries'} for k, v in rowarray_list.items()]

    return json.dumps(j, indent=4)


@app.route('/free_search', methods=['GET'] )
def free_search():
    free = request.args.get('term', '', type=str)

    rows = db.freeSearch(free)

    j = [{'id': id, 'label': name + ", " + location + ", " + city + ", " + country, 'value': name + ", " + location + ", " + city + ", " + country} for id, name, location, city, country in rows]

    return json.dumps(j, indent=4)

@app.route('/search_location', methods=['GET'] )
def search_location():
    location = request.args.get('term', '', type=str)

    rows = db.getLocations(location)

    j = [{'id': id, 'label': name, 'value': name} for id, name in rows]

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

        return db.getConcert(id)

    return ''


@app.route('/artist', methods=['GET'] )
def get_artist():

    id = request.args.get('id', '', type=int)

    return db.getArtist(id)


@app.route('/add_concert', methods=['GET', 'POST'])
def add_concert():
    if session['is_admin'] is False:
        return home()

    if request.method == 'GET':
        return render_template("add_concert.html")

    name = request.form.get('name', '', type=str)
    capacity = request.form.get('capacity', '', type=int)
    location_id = request.form.get('location_id', '', type=int)
    artists = request.form.get('artists', '', type=str).split(',')
    start = request.form.get('start', '', type=str).replace('- ','')
    end = request.form.get('end', '', type=str).replace('- ','')

    start = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.mktime(time.strptime(start, '%d %B %Y %H:%M'))))
    end = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.mktime(time.strptime(end, '%d %B %Y %H:%M'))))

    id = db.addConcert(name, capacity,artists,start,end,location_id)

    return '{"id" : "' + str(id) + '"}'

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
    return '[]' #db.getHotConcerts()




def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

@app.route('/find2', methods=['GET', 'POST'])
def advanced_search2():

    concert_id = request.args.get('concert_id')
    artist_id = request.args.get('artist_id')

    if concert_id:
        return db.getConcert(concert_id)

    if artist_id:
        return db.getConcertsByArtist(artist_id)

    return '[]'




# ================================
# ===== Users Options ======
# ================================
@app.route('/buy_tickets', methods=['GET', 'POST'])
def buy_tickets():
    if (session['logged_in']) :


        form = (request.form)
        if request.method == 'GET':
            quantity = request.args.get('quantity');#form.quantity.data;
            catagory_id = 1#request.args.get('catagory_id');
            concert_id = request.args.get('concert_id');
            user_id = session['user_id'];

            isSuccess = db.buy_ticket(quantity,catagory_id,user_id,concert_id)

            return isSuccess
    else:
        return 0;


@app.route("/recommendations", methods=['GET', 'POST'])
def recommendations():
    if session['logged_in']:
        top_5_genres= db.get_recommendations(session['username'])
        cur = get_db().cursor()

        print(len(top_5_genres))
        if len(top_5_genres) == 0:
            top_5_genres = db.get_all_genre()

        # Searching for top-10 gigs base on user's country and user's age
        records = db.get_top_10_country_age_user(session['country_id'], session['age'],top_5_genres)

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



        try:
            db.insert_user(form.username.data, form.password.data)

        except Exception as e:
            s = str(e)
            print(s)
            if 'UNIQUE' in s:
                return '1'
            return '2'
        user= db.select_user(form.username.data, form.password.data)

        if len(user) != 0:
            record = list(user).pop(0)
            session['logged_in'] = True
            session['username'] = record[0]
            session['is_admin'] = record[1]
            session['user_id'] = record[2]
            return '0'

        return '2'

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
            session['is_admin'] = record[1]
            session['user_id'] = record[2]
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