
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

    def buy_ticket(self,quantity,category,user_id,concert_id):
        cur = self.get_db().cursor()
        cur.execute("SELECT capacity FROM concert WHERE id = %s",
                    (concert_id))
        concert_data = list(cur.fetchall()).pop(0)
        if int(concert_data[0]) > 0:
            #try:
                cur.execute("INSERT INTO user_concert (user_id,like_concert,quantity,concert_id) VALUES (%s,%s,%s,%s)",
                        (user_id, 0, quantity, concert_id,))

                cur.execute("UPDATE concert SET capacity = (capacity - 1) WHERE id = %s",
                            (concert_id,))  # Capacity update after purchase

                cur.connection.commit()
                return '1'

            #except:
            #    return '0'
        elif int(concert_data[0]) == 0:
            return '0'
        #add concert to user_concert table


        #update the capacity of the ticket in the concert
        #user = cur.fetchall()
        #return user

    def login(self, username, password):
        cur = self.get_db().cursor()
        cur.execute("SELECT username, is_admin, id FROM user WHERE username = %s AND password = %s ",
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

    def getPersonalTikets(self, user_id):
        cur = self.get_db().cursor()
        # Searching for top-10 gigs base on user's city and user's age
        cur.execute(
            "SELECT concert.name, concert.id "
            "FROM concert,user_concert "
            "WHERE user_concert.concert_id = concert.id "
            "AND user_concert.user_id = %s "
            , (user_id, ))
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

        s = self.sqlToJson(cur.fetchall(), cur.description)
        concert = json.loads(s)

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
        cur.execute("INSERT INTO concert(name,capacity,start,end,location_id,tickets_left) VALUES(%s,%s,%s,%s,%s,%s)", (name,capacity,start,end,location_id,capacity))
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
            "WHERE concert.name like %s or location.name like %s or city.name like %s or country.name like %s LIMIT 5 ",
            ('%' + free + '%','%' + free + '%','%' + free + '%','%' + free + '%',))
        return cur.fetchall()

    def getLocations(self, location):
        cur = self.get_db().cursor()
        cur.execute(
            "select  location.id as id, concat(location.name, ', ', city.name , ', ' , country.name) as name " 
            "from location	inner join	city "
            "				on			location.city_id = city.id "
            "				and			location.name like %s "
            "				inner join	country "
            "				on			city.country_id = country.id",
            ('%' + location + '%',))
        return cur.fetchall()

    def sqlToJson(self, records, columns):
        result = [{columns[index][0]: column for index, column in enumerate(value)} for value in records]
        try:
            return json.dumps(result, indent=4, sort_keys=True, default=str)
        except:
            return json.dumps(result)

    def json_serial(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    def getHotConcerts(self):
        cur = self.get_db().cursor()

        cur.execute(
            "select artist.id, artist.name, concert_id "
            "from  artist	inner join	concert_artist "
            "               on			artist.id = concert_artist.artist_id "
            "               and			concert_artist.concert_id in ("
            "                                                           select  concert_id "
            "                                                           from    concert_artist"
            "                                                           where   artist_id = %s) "
            "ORDER BY concert_id")

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
            "               inner join  concert_user    "
            "               on          concert_user.concert_id = concert.id "
            "order by concert.id LIMIT 5")

        concert = json.loads(self.sqlToJson(cur.fetchall(), cur.description))

        return json.dumps({'concerts': concert, 'artists': artists}, default=self.json_serial)


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
            "SELECT genre_name"
            ",SUM(CASE WHEN date =  '2018-11' THEN count1  ELSE 0 END)  '2018-11'"
             ",SUM(CASE WHEN date =  '2018-12' THEN count1  ELSE 0 END)  '2018-12'"
            ", SUM(CASE WHEN date =  '2019-01' THEN count1 ELSE 0 END)  '2019-01'"
            ", SUM(CASE WHEN date =  '2019-02' THEN count1  ELSE 0 END)  '2019-02'"
            ",SUM(CASE WHEN date =  '2019-03' THEN count1  ELSE 0 END)  '2019-03'"
            ", SUM(CASE WHEN date =  '2019-04' THEN count1  ELSE 0 END)  '2019-04'"
            ", SUM(CASE WHEN date =  '2019-05' THEN count1  ELSE 0 END)  '2019-05'"
            ", SUM(CASE WHEN date =  '2019-06' THEN count1 ELSE 0  END)  '2019-06'"
            ",SUM(CASE WHEN date =  '2019-07' THEN count1  ELSE 0 END)  '2019-07'"
            ", SUM(CASE WHEN date =  '2019-08' THEN count1  ELSE 0 END)  '2019-08'"
            " , SUM(CASE WHEN date =  '2019-09' THEN count1  ELSE 0 END)  '2019-09'"
            ", SUM(CASE WHEN date =  '2019-10' THEN count1  ELSE 0 END)  '2019-10'"
       
            "FROM (SELECT g.name as genre_name,DATE_FORMAT(c.start, '%Y-%m') as date, count(c.id)  as count1 "
            "FROM concert c join concert_artist ca "
            "on c.id = ca.concert_id "
            "join  artist a  "
            "on a.id = ca.artist_id "
            "join genre g "
            "on a.genre_id = g.id "

            "where (substr(a.name, 1, 1) > 'A' and substr(a.name, 1, 1)< 'Z') or (substr(a.name, 1, 1) > 'a' and substr(a.name, 1, 1) < 'z')"
            "Group by g.name ,DATE_FORMAT(c.start, '%Y-%m')"
            # "having count(c.id)>=100" 
            ") concerts1 "
            "GROUP BY genre_name")
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
            "group by artist_name,artist_id "
            "having count(*)>1 ")

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
    def selectCities(self,filter):
        cur = self.get_db().cursor()
        cur.execute("SELECT city.id, city.name, country.name "
                    "FROM city "
                    "INNER JOIN country "
                    "ON city.country_id = country.id "
                    "AND city.name like %s "
                    "LIMIT 5", ('%' + filter + '%',))
        rows = cur.fetchall()
        return rows
    def selectCitiesArtists(self,filter,artist):
        cur = self.get_db().cursor()
        cur.execute("SELECT city.id, city.name, country.name "
                    "FROM city "
                    "INNER JOIN country "
                    "ON city.country_id = country.id "
                    "AND city.name like %s "
                    "inner join location "
                    "ON location.city_id = city.id "                                    
                    "INNER JOIN concert "
                    "on         location.id = concert.location_id "
                    "INNER join concert_artist "
                    "on         concert_artist.concert_id = concert_id "
                    "INNER JOIN artist "
                    "ON concert_artist.artist_id = artist.id "
                    "AND artist.id = %s "
                    "LIMIT 5", ('%' + filter + '%', artist ))
        rows = cur.fetchall()
        return rows

    def selectCountries(self, filter):
        cur = self.get_db().cursor()
        cur.execute("SELECT country.id, country.name "
                    "FROM country "
                    "WHERE country.name like %s "
                    "LIMIT 5", ('%' + filter + '%',))
        rows = cur.fetchall()
        return rows

    def selectCountriesArtists(self, filter, artist):
        cur = self.get_db().cursor()
        cur.execute("SELECT country.id, country.name "
                    "FROM city "
                    "INNER JOIN country "
                    "ON city.country_id = country.id "
                    "AND country.name like %s "
                    "inner join location "
                    "ON location.city_id = city.id "
                    "INNER JOIN concert "
                    "on         location.id = concert.location_id "
                    "INNER join concert_artist "
                    "on         concert_artist.concert_id = concert_id "
                    "INNER JOIN artist "
                    "ON concert_artist.artist_id = artist.id "
                    "AND artist.id = %s "
                    "LIMIT 5", ('%' + filter + '%', artist,))

        rows = cur.fetchall()
        return rows

    def get_recommendations(self,username):
        cur = self.get_db().cursor()
        # We want to get the most popular genre by the user
        # At first, We are looking for the number of tickets for each artist, Then we get there genre
        # And in the end we group the number of tickets together for each genre
        cur.execute("SELECT genre.genre_id, SUM(counter.job) as 'number_of_tickets' "
                    "FROM artist,genre, "
                    "(SELECT COUNT(user_concert.artist_id) AS 'job', user_concert.artist_id AS 'artist_id' "
                    "FROM user_concert,concert,artist "
                    "WHERE user_concert.artist_id = concert.artist_id AND user_concert.date_time = concert.date_time "
                    "AND concert.artist_id = artist.id "
                    "AND user_concert.username = %s "
                    "GROUP BY concert.artist_id ORDER BY job DESC) AS counter "
                    "WHERE counter.artist_id = artist.id AND artist.genre_id = genre.genre_id "
                    "GROUP BY genre.genre_id ORDER BY number_of_tickets DESC LIMIT 5"
                    , (username))
        top_5_genres = [item[0] for item in list(cur.fetchall())]
        return top_5_genres

    def get_all_genre(self):
        cur = self.get_db().cursor()
        cur.execute("SELECT genre.genre_id FROM genre")
        top_5_genres = list(cur.fetchall())
        return top_5_genres

    def get_top_10_country_age_user(self,country_id, age,top_5_genres):
        cur = self.get_db().cursor()
        cur.execute("SELECT artist.name, concert.date_time, city.name, country.country.name, "
                    "genre.genre_name, concert.age_limit, concert.price, concert.capacity "
                    "FROM city, concert, artist, genre, country "
                    "WHERE concert.city_id = city.id AND country.id = city.country_id "
                    "AND concert.artist_id = artist.id AND artist.genre_id = genre.genre_id "
                    "AND city.country_id = %s AND concert.age_limit <= %s AND genre.genre_id IN %s "
                    "ORDER BY concert.price ASC LIMIT 10"
                    , (country_id, age,top_5_genres))
        records = cur.fetchall()
        return records

    def insert_user(self,username,password):
        cur = self.get_db().cursor()
        cur.execute("INSERT INTO user (username,password) VALUES (%s,%s)", (username,password))
        cur.connection.commit()

    def select_user(self,username, password):
        cur = self.get_db().cursor()
        cur.execute("SELECT username, is_admin, id FROM user WHERE username = %s AND password = %s ",
                    (username, password))
        user = cur.fetchall()
        return user