from flask import g
import json
from datetime import date, datetime
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
            "select artist.artist_id, artist.artist_name "
            "from  artist	inner join	concert_artist "
            "               on			artist.artist_id = concert_artist.artist_id "
            "               and			concert_artist.concert_id = ? ",
            (id,))

        artists = self.sqlToJson(cur.fetchall(), cur.description)

        cur.execute(
            "SELECT concert.name, concert.capacity, concert.start, concert.end, concert.id "
            "FROM concert "
            "WHERE concert.id = ? ",
            (id,))

        concert = json.loads(self.sqlToJson([cur.fetchone()],cur.description))

        concert[0]['artists'] = artists

        return json.dumps(concert[0], default=self.json_serial)

    def getArtist(self, id):
        cur = self.get_db().cursor()

        cur.execute(
            "select artist.artist_id, artist.artist_name "
            "from  artist	"
            "where artist_id = ? ",
            (id,))

        artist = self.sqlToJson(cur.fetchall(), cur.description)

        return json.dumps(artist, default=self.json_serial)

    def addConcert(self, name, capacity, artists, start, end):
        cur = self.get_db().cursor()
        cur.execute("INSERT INTO concert(name,capacity,start,end) VALUES(?,?,?,?)", (name,capacity,start,end))
        cur.connection.commit()

        id = cur.lastrowid
        for artist in artists:
            cur.execute("INSERT INTO concert_artist(concert_id,artist_id) VALUES(?,?)", (id, artist))

        cur.connection.commit()

        return id

    def freeSearch(self, free):
        cur = self.get_db().cursor()
        cur.execute(
            "SELECT concert.id,concert.name, location.name, city.city_name, country.country_name  "
            "FROM concert   inner join  location"
            "               on          location.id = concert.location_id "
            "               inner join  city "
            "               on          city.city_id = location.city_id "
            "               inner join  country "
            "               on          city.country_id = country.country_id "
            "WHERE concert.name like ? ",
            ('%' + free + '%',))
        return cur.fetchall()

    def getLocations(self, location):
        cur = self.get_db().cursor()
        cur.execute(
            "select location.id, location.name || ', ' || city.city_name || ', ' || country.country_name " 
            "from location	inner join	city "
            "				on			location.city_id = city.city_id "
            "				and			location.name like ? "
            "				inner join	country "
            "				on			city.country_id = country.country_id",
            ('%' + location + '%',))
        return cur.fetchall()

    def sqlToJson(self, records, columns):
        result = [{columns[index][0]: column for index, column in enumerate(value)} for value in records]
        return json.dumps(result, default=self.json_serial)

    def json_serial(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type ? not serializable" % type(obj))

    def getHotConcerts(self):
        cur = self.get_db().cursor()

        cur.execute(
            "SELECT concert.name, concert.capacity, concert.start, concert.end, concert.id "
            "FROM concert "
            "Limit 5")

        concerts = json.loads(self.sqlToJson(cur.fetchall(), cur.description))

        '''
        cur.execute(
            "select artist.artist_id, artist.artist_name "
            "from  artist	inner join	concert_artist "
            "               on			artist.artist_id = concert_artist.artist_id "
            "               and			concert_artist.concert_id = ? ",
            (id,))

        artists = self.sqlToJson(cur.fetchall(), cur.description)
        '''


        #concert[0]['artists'] = artists

        return json.dumps(concerts, default=self.json_serial)