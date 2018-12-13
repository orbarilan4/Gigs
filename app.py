from flask import Flask, render_template, url_for, request, flash, redirect, session
from flaskext.mysql import MySQL
from forms import AdvancedSearch, RegistrationForm, LoginForm, UpdateProfileForm, AddDelConcert
import numpy as np
import json
from initialization_scripts.utils import xstr,get_record

mysql = MySQL()

# db_connection.mysql_db_connection()
app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = '85.10.205.173'
app.config['MYSQL_DATABASE_USER'] = 'orbari123456'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Oliver123'
app.config['MYSQL_DATABASE_DB'] = 'music321'
app.config['SECRET_KEY'] = 'f9bf78b9a18ce6d46a0cd2b0b86df9da'
mysql.init_app(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


# ================================
# ===== User Page Options ======
# ================================
@app.route("/show_profile", methods=['GET', 'POST'])
def show_profile():
    if session['logged_in'] is False:
        return render_template('index.html')
    return render_template('show_profile.html')


@app.route("/update_profile", methods=['GET', 'POST'])
def update_profile():
    if session['logged_in']:
        form = UpdateProfileForm(request.form)
        if request.method == 'POST' and form.validate():
            cur = mysql.get_db().cursor()
            cur.execute("SELECT city_name, city_id FROM city WHERE city_name = %s", form.city.data) # Checking if the city exist
            city_record = list(cur.fetchall())
            if city_record:
                city_record = city_record.pop(0)
                cur.execute("UPDATE user SET user.age = %s , user.city_id = %s, user.picture = %s  WHERE user.username = %s",
                            (form.age.data, city_record[1], form.picture.data, session['username']))
                mysql.get_db().commit()
                session['age'] = form.age.data
                session['city_name'] = form.city.data.title()
                session['city_id'] = city_record[1]
                session['picture'] = form.picture.data
                cur.execute("SELECT city.city_name, country.country_name FROM city,country "
                            "WHERE country.country_id = city.country_id AND city.city_id = %s"
                            , session['city_id'])  # Get city and country name from user

                place = list(cur.fetchall()).pop(0)
                session['country_name'] = place[1]
                flash(f'Your account updated!', 'success')
                return show_profile()
            elif len(city_record) == 0:
                flash(f'The entered city does not exist!', 'error')
                return redirect(url_for('update_profile'))
    else:
        return render_template('index.html')
    return render_template('update_profile.html', form=form)


@app.route("/personal_tickets", methods=['GET', 'POST'])
def personal_tickets():
    if session['logged_in']:
        cur = mysql.get_db().cursor()
        # Searching for top-10 gigs base on user's city and user's age
        cur.execute(
            "SELECT artist.artist_name, concert.date_time, city.city_name, country.country_name, genre.genre_name "
            "FROM city, concert, artist,user_concert,country,genre "
            "WHERE concert.city_id = city.city_id "
            "AND concert.artist_id = artist.artist_id AND country.country_id = city.country_id "
            "AND user_concert.artist_id = concert.artist_id AND user_concert.date_time = concert.date_time "
            "AND artist.genre_id = genre.genre_id AND user_concert.username = %s ORDER BY concert.price "
            , session['username'])
        records = cur.fetchall()
    else:
        return render_template('index.html')
    return render_template('result.html', orders=False, records=records)


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
            cur = mysql.get_db().cursor()
            colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA", "#ABCDEF", "#DDDDDD", "#ABCABC"]
            # Checking if the entered country is exist
            cur.execute("SELECT country_name FROM country WHERE country_name = %s", form.country.data)
            country = cur.fetchall()
            if len(country) == 0:
                flash(f'The entered country does not exist!', 'error')
                return redirect(url_for('analytics'))
            else:
                session['country_input_exists'] = form.country.data
                # Searching for top-10 host cities in selected (by user) country
                cur.execute("SELECT city.city_name,counter.job FROM city AS city, "
                            "(SELECT concert.city_id,count(*) AS 'job' FROM concert, city, country "
                            "WHERE concert.city_id = city.city_id AND city.country_id = country.country_id "
                            "AND country.country_name = COALESCE(%s,country.country_name) "
                            "GROUP BY concert.city_id "
                            "ORDER BY job DESC LIMIT 10) AS counter "
                            "WHERE counter.city_id = city.city_id", form.country.data)
                freq_city = np.array(list(cur.fetchall()), dtype=np.dtype('object,int'))

                # Searching for top-10 hosted artists in selected (by user) country
                cur.execute("SELECT artist.artist_name,counter.job FROM artist AS artist, "
                            "(SELECT concert.artist_id,count(*) AS 'job' FROM concert, city, country "
                            "WHERE concert.city_id = city.city_id AND city.country_id = country.country_id "
                            "AND country.country_name = COALESCE(%s,country.country_name) "
                            "GROUP BY concert.artist_id "
                            "ORDER BY job DESC LIMIT 10) AS counter "
                            "WHERE counter.artist_id = artist.artist_id", form.country.data)
                freq_artist = np.array(list(cur.fetchall()), dtype=np.dtype('object,int'))

                # Age limit distribution in selected (by user) country
                cur.execute("SELECT concert.age_limit,count(*) AS 'job' FROM concert, city, country "
                            "WHERE concert.city_id = city.city_id AND city.country_id = country.country_id "
                            "AND country.country_name = COALESCE(%s,country.country_name) "
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
    filter = request.args.get('term', '', type=str)
    cur = mysql.get_db().cursor()
    cur.execute("SELECT city_id, city_name, country_name "
                "FROM city "
                "INNER JOIN country "
                "ON city.country_id = country.country_id "
                "AND city_name like '%s' "                
                "LIMIT 5" % ('%' + filter + '%'))
    rows = cur.fetchall()

    cur.execute("SELECT country_id, country_name "
                "FROM country "
                "WHERE country_name like '%s' "
                "LIMIT 5" % ('%' + filter + '%'))
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


@app.route('/add_concert', methods=['GET', 'POST'])
def add_concert():
    if session['is_admin'] and session['logged_in']:
        form = AddDelConcert(request.form)
        if request.method == 'POST' and form.validate():
            cur = mysql.get_db().cursor()
            cur.execute("SELECT city_name, city_id FROM city WHERE city_name = %s",form.city.data) # Checking if the city exist
            city_record = cur.fetchall()
            cur.execute("SELECT artist_name, artist_id FROM artist WHERE artist_name = %s",form.artist.data)  # Checking if the artist exist
            artist_record = cur.fetchall()
            if len(city_record) != 0 and len(artist_record) != 0:
                try:
                    cur.execute(
                        "INSERT INTO concert (artist_id,city_id,date_time,capacity,age_limit,price)"
                        "VALUES (%s,%s,%s,%s,%s,%s)",
                        (int(list(artist_record).pop(0)[1]), int(list(city_record).pop(0)[1]),
                         form.date.data, form.capacity.data, form.age_limit.data,form.price.data))
                    mysql.get_db().commit()
                    flash(f'New gig created successfully!', 'success')
                    return redirect(url_for('add_concert'))
                except:
                    flash(f'The artist has already played on this date', 'error')
                    return redirect(url_for('add_concert'))
            elif len(city_record) == 0:
                flash(f'The entered city does not exist!', 'error')
                return redirect(url_for('add_concert'))
            elif len(artist_record) == 0:
                flash(f'The entered artist does not exist!', 'error')
                return redirect(url_for('add_concert'))
    else:
        return render_template("index.html")
    return render_template("add_concert.html", form=form)


@app.route('/del_concert', methods=['GET', 'POST'])
def del_concert():
    if session['is_admin'] and session['logged_in']:
        form = AddDelConcert(request.form)
        if request.method == 'POST':
            cur = mysql.get_db().cursor()
            cur.execute("SELECT artist_name, artist_id FROM artist WHERE artist_name = %s", form.artist.data)  # Checking if the artist exist
            artist_record = cur.fetchall()
            if len(artist_record) != 0:
                artist = list(artist_record).pop(0)
                cur.execute("SELECT date_time, artist_id FROM concert WHERE artist_id= %s AND date_time = %s",
                            (int(artist[1]),form.date.data))  # Checking if the concert exist
                concert_record = cur.fetchall()
                if len(concert_record) != 0:
                    cur.execute(
                        "DELETE FROM user_concert WHERE artist_id = %s AND date_time = %s",
                        (int(artist[1]), form.date.data))
                    cur.execute(
                        "DELETE FROM concert WHERE artist_id = %s AND date_time = %s",
                        (int(artist[1]), form.date.data))
                    mysql.get_db().commit()
                    flash(f"{artist[0]}'s gig on {form.date.data} canceled successfully!", 'success')
                    print(form.date.data)
                    return redirect(url_for('del_concert'))
                else:
                    flash(f"There is no {artist[0]}'s gig on {form.date.data}", 'error')
                    return redirect(url_for('del_concert'))
            elif len(artist_record) == 0:
                flash(f'The entered artist does not exist!', 'error')
                return redirect(url_for('del_concert'))
    else:
        return render_template("index.html")
    return render_template("del_concert.html", form=form)


# ================================
# ===== General Options ======
# ================================
@app.route('/advanced_search', methods=['GET', 'POST'])
def advanced_search():
    form = AdvancedSearch(request.form)
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
        cur = mysql.get_db().cursor()

        cur.execute(
            "SELECT artist.artist_name ,concert.date_time , city.city_name, country.country_name, "
            "genre.genre_name, concert.age_limit , concert.price, concert.capacity "
            "FROM city, concert, artist, genre, country "
            "WHERE concert.city_id = city.city_id AND country.country_id = city.country_id "
            "AND concert.artist_id = artist.artist_id AND artist.genre_id = genre.genre_id "
            "AND ((artist.artist_name LIKE COALESCE(%s,artist.artist_name)) "
            "AND (concert.date_time = COALESCE(%s,concert.date_time)) "
            "AND (country.country_name LIKE COALESCE(%s,country.country_name)) "
            "AND (city.city_name LIKE COALESCE(%s,city.city_name)) "
            "AND (genre.genre_name LIKE COALESCE(%s,genre.genre_name)) "
            "AND (concert.age_limit >= COALESCE(%s,concert.age_limit)) "
            "AND (concert.age_limit <= COALESCE(%s,concert.age_limit)) "
            "AND (concert.price >= COALESCE(%s,concert.price)) "
            "AND (concert.price <= COALESCE(%s,concert.price)) "
            ")ORDER BY concert.price LIMIT 20",
            (("%" + xstr(artist) + "%"), date, ("%" + xstr(country) + "%"), ("%" + xstr(city) + "%"), ("%" + xstr(genre) + "%"),
             int(min_age), int(max_age), int(min_price), int(max_price)))
        records = cur.fetchall()
        if len(records) == 0:
            return render_template("sorry.html")
        else:
            return render_template("result.html", records=records, orders=True)
    return render_template("advanced_search.html", form=form)


# ================================
# ===== Users Options ======
# ================================
@app.route('/buy_tickets', methods=['GET', 'POST'])
def buy_tickets():
    if request.method == 'POST':
        for record in request.form.getlist('checks'):
            print(record)
            cur = mysql.get_db().cursor()
            # Casting
            record = get_record(record)
            # Get artist id
            cur.execute("SELECT artist.artist_name, artist.artist_id FROM artist,genre "
                        "WHERE genre.genre_id = artist.genre_id AND artist_name = %s AND genre_name = %s", (record[0], record[4]))
            artist_record = list(cur.fetchall()).pop(0)
            # Get capacity and age limit for concert
            cur.execute("SELECT capacity,age_limit FROM concert WHERE artist_id = %s AND date_time = %s",
                        (artist_record[1], record[1]))
            concert_data = list(cur.fetchall()).pop(0)

            # If there are tickets available
            if int(concert_data[0]) > 0 and int(session['age']) >= int(concert_data[1]):
                try:
                    cur.execute("INSERT INTO user_concert (username,artist_id,date_time) VALUES (%s,%s,%s)",
                                (session['username'],artist_record[1] , record[1])) # New Add ticket to user_concert
                    cur.execute("UPDATE concert SET capacity = (capacity - 1) WHERE artist_id = %s AND date_time = %s",
                                (artist_record[1], record[1]))  # Capacity update after purchase
                    mysql.get_db().commit()
                    flash(f"You bought some tickets ! You can view them on your profile", 'success')
                except:
                    flash(f"Already have a ticket for {record[0]}'s gig on {record[1]} !", 'warning')
            elif int(concert_data[0]) == 0:
                flash(f"No tickets available for {record[0]}'s gig on {record[1]} !", 'error')
            elif int(concert_data[1]) > int(session['age']):
                flash(f"You are under age for {record[0]}'s gig on {record[1]} !", 'error')
    return render_template("index.html")


@app.route("/recommendations", methods=['GET', 'POST'])
def recommendations():
    if session['logged_in']:
        cur = mysql.get_db().cursor()
        # We want to get the most popular genre by the user
        # At first, We are looking for the number of tickets for each artist, Then we get there genre
        # And in the end we group the number of tickets together for each genre
        cur.execute("SELECT genre.genre_id, SUM(counter.job) as 'number_of_tickets' "
                    "FROM artist,genre, "
                    "(SELECT COUNT(user_concert.artist_id) AS 'job', user_concert.artist_id AS 'artist_id' "
                    "FROM user_concert,concert,artist "
                    "WHERE user_concert.artist_id = concert.artist_id AND user_concert.date_time = concert.date_time "
                    "AND concert.artist_id = artist.artist_id "
                    "AND user_concert.username = %s "
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
                    "AND city.country_id = %s AND concert.age_limit <= %s AND genre.genre_id IN %s "
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
    if session['logged_in'] is False:
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            cur = mysql.get_db().cursor()
            cur.execute("SELECT city_name, city_id FROM city WHERE city_name = %s", form.city.data) # Checking if the city exist
            city_record = cur.fetchall()
            cur.execute("SELECT is_admin,username FROM user WHERE username = %s", form.username.data) # Checking if user doesnt exist
            username_record = cur.fetchall()
            if len(city_record) != 0 and len(username_record) == 0:
                cur.execute("INSERT INTO user (username,age,city_id,password,is_admin,picture) VALUES (%s,%s,%s,%s,%s,%s)",
                            (form.username.data, form.age.data, int(list(city_record).pop(0)[1]),
                             form.password.data,False,"http://meng.uic.edu/wp-content/uploads/sites/92/2018/07/empty-profile.png"))
                mysql.get_db().commit()
                flash(f'Account created for {form.username.data}!', 'success')
                return redirect(url_for('home'))
            elif len(city_record) == 0:
                flash(f'The entered city does not exist!', 'error')
                return redirect(url_for('register'))
            elif len(username_record) != 0:
                flash(f'Username already exists!', 'error')
                return redirect(url_for('register'))
    else:
        return render_template('index.html')
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        cur = mysql.get_db().cursor()
        cur.execute("SELECT username, city_id, age, is_admin, picture FROM user WHERE username = %s AND password = %s ",
                    (form.username.data,form.password.data))
        user = cur.fetchall()
        if len(user) != 0:
            flash(f'You have been logged in !', 'success')
            record = list(user).pop(0)
            session['logged_in'] = True
            session['username'] = record[0]
            session['city_id'] = record[1]
            session['age'] = record[2]
            session['is_admin'] = record[3]
            session['picture'] = record[4]
            cur.execute("SELECT city.city_name, country.country_name,country.country_id FROM city,country "
                        "WHERE country.country_id = city.country_id AND city.city_id = %s"
                        , session['city_id'])  # Get city and country name from user
            place = list(cur.fetchall()).pop(0)
            session['city_name'] = place[0]
            session['country_name'] = place[1]
            session['country_id'] = place[2]
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Please check username and password !', 'error')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['is_admin'] = False
    return home()


if __name__ == "__main__":
    app.debug = True
    app.run()
