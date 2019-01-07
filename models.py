from flask import g
import json
from datetime import date, datetime


class modelDB:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_db(self):
        return self.mysql.connect()

    def close_connection(self, exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    def login(self, username, password):
        cur = self.get_db().cursor()
        cur.execute("SELECT username, is_admin FROM user WHERE username = %s AND password = %s ",
                    (username, password))
        user = cur.fetchall()
        return user

    def getRecord(self, city):
        cur = self.get_db().cursor()
        cur.execute("SELECT name, id FROM city WHERE name = %s",
                    city)  # Checking if the city exist
        city_record = list(cur.fetchall())
        return city_record

    def updateRecord(self,age, city, pic, username):
        pass

    def getPersonalTikets(self, username):
        cur = self.get_db().cursor()
        # Searching for top-10 gigs base on user's city and user's age
        cur.execute(
            "SELECT concert.name, concert.id "
            "FROM concert,user_concert "
            "WHERE user_concert.concert_id = concert.id "
            "AND user_concert.username = %s "
            , (username, ))
        records = cur.fetchall()
        return records

    def findConcerts(self):
        cur = self.get_db().cursor()

    def searchArtist(self, artist):
        cur = self.get_db().cursor()
        cur.execute("SELECT id, name "
                    "FROM artist "
                    "WHERE name like %s "
                    "LIMIT 5", (('%' + artist + '%'),))
        records = list(cur.fetchall())
        return records

    def deleteConcert(self, id):
        cur = self.get_db().cursor()
        cur.execute("DELETE FROM concert WHERE id = %s", (id,))
        cur.connection.commit()

    def getConcert(self, id):
        cur = self.get_db().cursor()

        cur.execute(
            "select artist.id, artist.name, concert_id "
            "from  artist	inner join	concert_artist "
            "               on			artist.id = concert_artist.artist_id "
            "               and			concert_artist.concert_id = %s ",
            (id,))

        artists = self.sqlToJson(cur.fetchall(), cur.description)

        cur.execute(
            "SELECT concert.name, concert.capacity, concert.start, concert.end, concert.id, location.name as location, city.name as city, country.name as country "
            "FROM concert   inner join  location "
            "               on          concert.location_id = location.id "
            "               inner join  city "
            "               on          location.city_id = city.id "
            "               inner join  country "
            "               on          city.country_id = country.id "
            "WHERE concert.id = %s ",
            (id,))


        concert = json.loads(self.sqlToJson(cur.fetchall(), cur.description))

        return json.dumps({'concerts' : concert, 'artists' : artists}, default=self.json_serial)

    def getArtist(self, id):
        cur = self.get_db().cursor()

        cur.execute(
            "select artist.id, artist.name "
            "from  artist	"
            "where id = %s ",
            (id,))

        artist = self.sqlToJson(cur.fetchall(), cur.description)

        return json.dumps(artist, default=self.json_serial)

    def addConcert(self, name, capacity, artists, start, end,location_id):
        cur = self.get_db().cursor()
        cur.execute("INSERT INTO concert(name,capacity,start,end,location_id) VALUES(%s,%s,%s,%s,%s)", (name,capacity,start,end,location_id))
        cur.connection.commit()

        id = cur.lastrowid
        for artist in artists:
            cur.execute("INSERT INTO concert_artist(concert_id,artist_id) VALUES(%s,%s)", (id, artist))

        cur.connection.commit()

        return id

    def freeSearch(self, free):
        cur = self.get_db().cursor()
        cur.execute(
            "SELECT concert.id,concert.name, location.name, city.name, country.name  "
            "FROM concert   inner join  location"
            "               on          location.id = concert.location_id "
            "               inner join  city "
            "               on          city.id = location.city_id "
            "               inner join  country "
            "               on          city.country_id = country.id "
            "WHERE concert.name like %s ",
            ('%' + free + '%',))
        return cur.fetchall()

    def getLocations(self, location):
        cur = self.get_db().cursor()
        cur.execute(
            "select location.id, location.name || ', ' || city.name || ', ' || country.name " 
            "from location	inner join	city "
            "				on			location.city_id = city.id "
            "				and			location.name like %s "
            "				inner join	country "
            "				on			city.country_id = country.id",
            ('%' + location + '%',))
        return cur.fetchall()

    def sqlToJson(self, records, columns):
        result = [{columns[index][0]: column for index, column in enumerate(value)} for value in records]
        return json.dumps(result, default=self.json_serial)

    def json_serial(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    def getHotConcerts(self):
        cur = self.get_db().cursor()

        cur.execute(
            "SELECT concert.name, concert.capacity, concert.start, concert.end, concert.id "
            "FROM concert "
            "Limit 5")

        concerts = json.loads(self.sqlToJson(cur.fetchall(), cur.description))

        '''
        cur.execute(
            "select artist.id, artist.name "
            "from  artist	inner join	concert_artist "
            "               on			artist.id = concert_artist.artist_id "
            "               and			concert_artist.concert_id = %s ",
            (id,))

        artists = self.sqlToJson(cur.fetchall(), cur.description)
        '''


        #concert[0]['artists'] = artists

        return json.dumps(concerts, default=self.json_serial)

    def getConcertsByArtist(self, artist_id):
        cur = self.get_db().cursor()

        cur.execute(
            "select artist.id, artist.name, concert_id "
            "from  artist	inner join	concert_artist "
            "               on			artist.id = concert_artist.artist_id "
            "               and			concert_artist.concert_id in ("
            "                                                           select  concert_id "
            "                                                           from    concert_artist"
            "                                                           where   artist_id = %s) "
            "ORDER BY concert_id",
            (artist_id,))

        artists = self.sqlToJson(cur.fetchall(), cur.description)

        cur.execute(
            "SELECT concert.name, concert.capacity, concert.start, concert.end, concert.id, location.name as location, city.name as city, country.name as country "
            "FROM concert   inner join  location"
            "               on          location.id = concert.location_id "
            "               inner join  city "
            "               on          city.id = location.city_id "
            "               inner join  country "
            "               on          city.country_id = country.id "
            "               inner join  concert_artist "
            "               on          concert_artist.concert_id = concert.id "
            "WHERE concert_artist.artist_id = %s ",
            (artist_id,))

        concert = json.loads(self.sqlToJson(cur.fetchall(), cur.description))

        return json.dumps({'concerts' : concert, 'artists' : artists}, default=self.json_serial)

    def analytics_get_concert_number_per_artist(self):
        cur = self.get_db().cursor()
        cur.execute(

            "SELECT a.name, count(c.name) "
            "FROM concert c join concert_artist ca "
            "on c.id = ca.concert_id "
            "join  artist a  on a.id = ca.artist_id " 
        
            "where (substr(a.name, 1, 1) > 'A' and substr(a.name, 1, 1)< 'Z') or (substr(a.name, 1, 1) > 'a' and substr(a.name, 1, 1) < 'z') " 
            "group by a.name "
            "order by count(c.name) desc limit 10 "
        )
        records = list(cur.fetchall())
        return records

    def analytics_get_concert_number_per_genre(self):
        cur = self.get_db().cursor()
        cur.execute(
            "SELECT g.name, count(c.id) "
            "FROM concert c join concert_artist ca "
            "on c.id = ca.concert_id "
            "join  artist a  "
            "on a.id = ca.artist_id "
            "join genre g " 
            "on a.genre_id = g.id " 
            "where (substr(a.name, 1, 1) > 'A' and substr(a.name, 1, 1)< 'Z') or (substr(a.name, 1, 1) > 'a' and substr(a.name, 1, 1) < 'z') " 
            "Group by g.name "
            # "having count(c.id)>=100 "
            " order by count(c.id) desc limit 20 "
        )
        records = list(cur.fetchall())
        return records

    def analytics_get_concert_number_per_genre_per_month(self):
        cur = self.get_db().cursor()
        cur.execute(
            #   "   SELECT g.genre_name,strftime('%Y-%m',c.date_time) as date, count(c.id) "
            # " FROM concert c join artist a "
            # " on c.artist_id = a.artist_id "
            # "  join genre g on a.genre_id = g.genre_id "
            #  " where (substr(a.artist_name, 1, 1) > 'A' and substr(a.artist_name, 1, 1)< 'Z') or (substr(a.artist_name, 1, 1) > 'a' and substr(a.artist_name, 1, 1) < 'z') "
            #  " Group by g.genre_name ,strftime('%Y-%m',c.date_time)"
            #  " having count(c.id)>=100"
            #  "  order by date desc")
            "SELECT concerts1.name"
            ", SUM(CASE WHEN date =  '2019-02' THEN count1 ELSE '222' END)  '2019-01'"
            ", SUM(CASE WHEN date =  '2019-02' THEN count1  ELSE '222' END)  '2019-02'"
            ",SUM(CASE WHEN date =  '2019-03' THEN count1  ELSE '222' END)  '2019-03'"
            ", SUM(CASE WHEN date =  '2019-04' THEN count1  ELSE '222' END)  '2019-04'"
            ", SUM(CASE WHEN date =  '2019-05' THEN count1  ELSE '222' END)  '2019-05'"
            ", SUM(CASE WHEN date =  '2019-06' THEN count1 ELSE '222'  END)  '2019-06'"
            ",SUM(CASE WHEN date =  '2019-07' THEN count1  ELSE '222' END)  '2019-07'"
            ", SUM(CASE WHEN date =  '2019-08' THEN count1  ELSE '222' END)  '2019-08'"
            " , SUM(CASE WHEN date =  '2019-09' THEN count1  ELSE '222' END)  '2019-09'"
            ", SUM(CASE WHEN date =  '2019-10' THEN count1  ELSE '222' END)  '2019-10'"
            ",SUM(CASE WHEN date =  '2019-11' THEN count1  ELSE '222' END)  '2019-11'"
            ", SUM(CASE WHEN date =  '2019-12' THEN count1 ELSE '222' END)  '2019-12' "
            "FROM (SELECT g.name,DATE_FORMAT(c.start, '%Y-%m') as date, count(c.id)  as count1 " 
            "FROM concert c join concert_artist ca "
            "on c.id = ca.concert_id "
            "join  artist a  "
            "on a.id = ca.artist_id "
            "join genre g "
            "on a.genre_id = g.id "
     
             "where (substr(a.name, 1, 1) > 'A' and substr(a.name, 1, 1)< 'Z') or (substr(a.name, 1, 1) > 'a' and substr(a.name, 1, 1) < 'z')" 
            "Group by g.name ,DATE_FORMAT(c.start, '%Y-%m')"
            #"having count(c.id)>=100" 
            ") concerts1 "
            "GROUP BY concerts1.name")
        records = list(cur.fetchall())
        return records

    def analytics_get_capacity_percent_per_artist(self):
        cur = self.get_db().cursor()
        cur.execute(
                "select artist_name,artist_id, avg(per.percent) from( "
                "SELECT a.name as artist_name,a.id as artist_id,c.name,c.capacity, count(uc.user_id), (count(uc.user_id)/c.capacity)*100 as percent "
                "FROM concert c join concert_artist ca "
                "on c.id = ca.concert_id "
                "join  artist a  on a.id = ca.artist_id "
                "join user_concert uc on c.id = uc.concert_id "
                "where (substr(a.name, 1, 1) > 'A' and substr(a.name, 1, 1)< 'Z') or (substr(a.name, 1, 1) > 'a' and substr(a.name, 1, 1) < 'z') " 
                "group by a.name,a.id,c.name, c.capacity "
                 ") per "
                "group by artist_name,artist_id")

        records = list(cur.fetchall())
        return records


    def analytics_get_capacity_percent_per_concert_per_artist(self):
        cur = self.get_db().cursor()
        cur.execute(

                "SELECT a.name as artist_name,a.id as artist_id,c.name,c.capacity, count(uc.user_id), (count(uc.user_id)/c.capacity)*100 as percent "
                "FROM concert c join concert_artist ca "
                "on c.id = ca.concert_id "
                "join  artist a  on a.id = ca.artist_id "
                "join user_concert uc on c.id = uc.concert_id "
                "where (substr(a.name, 1, 1) > 'A' and substr(a.name, 1, 1)< 'Z') or (substr(a.name, 1, 1) > 'a' and substr(a.name, 1, 1) < 'z') " 
                "group by a.name,a.id,c.name, c.capacity "
                )

        records = list(cur.fetchall())
        return records