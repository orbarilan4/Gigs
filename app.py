from flask import Flask, render_template, url_for, request ,redirect
from flaskext.mysql import MySQL
from wtforms import Form, StringField
import db_connection

mysql = MySQL()

# db_connection.mysql_db_connection()
app = Flask(__name__, static_url_path='/static')
app.config['MYSQL_DATABASE_HOST']='85.10.205.173'
app.config['MYSQL_DATABASE_USER']='orbarilan100'
app.config['MYSQL_DATABASE_PASSWORD']='R3hab123'
app.config['MYSQL_DATABASE_DB']='music123'
mysql.init_app(app)


@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')


@app.route("/data")
def data():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT city_id,city_name FROM city WHERE city_name ='TEL AVIV'")
    # cur.execute("SELECT city_id,city_name FROM city WHERE city_name ='TEL AVIV'")
    print(str(cur.fetchall()))
    return render_template('data.html')


@app.route('/search', methods=['GET', 'POST'] )
def search():
    if request.method == "POST":
        cur = mysql.get_db().cursor()
        cur.execute("SELECT city_id,city_name FROM city WHERE city_name = %s ", request.form['search'])
        return render_template("result.html", records=cur.fetchall())
    #return render_template('search.html')


class AdvancedSearch(Form):
    artist = StringField('Artist')
    city = StringField('City')
    country = StringField('Country')
    date = StringField('Date')
    genre = StringField('Genre')
    age = StringField('Age')
    min_price = StringField('Minimum Price')
    max_price = StringField('Maximum Price')


@app.route('/advanced_search',methods = ['GET','POST'])
def advanced_search():
    form = AdvancedSearch(request.form)
    if request.method == 'POST':
        artist = form.artist.data
        city = form.city.data
        country = form.country.data
        date = form.date.data
        genre = form.genre.data
        age = form.age.data
        min_price = form.min_price.data
        max_price = form.max_price.data
        cur = mysql.get_db().cursor()
        cur.execute("SELECT country_id,country_name FROM country WHERE country_name = %s ", country)
        return render_template("result.html", records=cur.fetchall())
    return render_template("advanced_result.html",form=form)


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run()
