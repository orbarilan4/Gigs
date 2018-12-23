from flask import g
import sqlite3


class modelDB:
    def __init__(self):
        self.DATABASE = 'db/gigs.db'

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.DATABASE)
        return db


    def close_connection(self, exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    def login(self, username, password):
        cur = self.get_db().cursor()
        cur.execute("SELECT username, city_id, age, is_admin, picture FROM user WHERE username = ? AND password = ? ",
                    (username, password))
        user = cur.fetchall()
        return user

    def getRecord(self, city):
        cur = self.get_db().cursor()
        cur.execute("SELECT city_name, city_id FROM city WHERE city_name = ?",
                    city)  # Checking if the city exist
        city_record = list(cur.fetchall())
        return city_record

    def updateRecord(self,age, city, pic, username):
        cur = self.get_db().cursor()
        cur.execute("UPDATE user SET user.age = ? , user.city_id = ?, user.picture = ?  WHERE user.username = ?",
                    (age, city, pic, username))

    def getPersonalTikets(self, username):
        cur = self.get_db().cursor()
        # Searching for top-10 gigs base on user's city and user's age
        cur.execute(
            "SELECT artist.artist_name, concert.date_time, city.city_name, country.country_name, genre.genre_name "
            "FROM city, concert, artist,user_concert,country,genre "
            "WHERE concert.city_id = city.city_id "
            "AND concert.artist_id = artist.artist_id AND country.country_id = city.country_id "
            "AND user_concert.artist_id = concert.artist_id AND user_concert.date_time = concert.date_time "
            "AND artist.genre_id = genre.genre_id AND user_concert.username = ? ORDER BY concert.price "
            , (username))
        records = cur.fetchall()
        return records

    def findConcerts(self):
        cur = self.get_db().cursor()