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
            "SELECT concert.name, concert.id "
            "FROM concert,user_concert "
            "WHERE user_concert.concert_id = concert.id "
            "AND user_concert.username = ? "
            , (username, ))
        records = cur.fetchall()
        return records

    def findConcerts(self):
        cur = self.get_db().cursor()

    def searchArtist(self, artist):
        cur = self.get_db().cursor()
        cur.execute("SELECT artist_id, artist_name "
                    "FROM artist "
                    "WHERE artist_name like ? "
                    "LIMIT 5", (('%' + artist + '%'),))
        records = list(cur.fetchall())
        return records

    def deleteConcert(self, id):
        cur = self.get_db().cursor()
        cur.execute("DELETE FROM concert WHERE id = ?", (id,))
        cur.connection.commit()

    def getConcert(self, id):
        cur = self.get_db().cursor()
        cur.execute(
            "SELECT concert.name, concert.capacity, concert.start, concert.end "
            "FROM concert "
            "WHERE concert.id = ? ",
            (id,))
        return (cur.fetchone(),cur.description)

    def addConcert(self, name, capacity):
        cur = self.get_db().cursor()
        cur.execute("INSERT INTO concert(name,capacity) VALUES(?,?)", (name,capacity))
        cur.connection.commit()