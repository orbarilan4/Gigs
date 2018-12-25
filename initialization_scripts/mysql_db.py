import csv
import sqlite3

def mysql_db():
    prefix = ''
    try:
        my_db = sqlite3.connect('db/gigs.db')
    except:
        prefix = '../'
        my_db = sqlite3.connect(prefix + 'db/gigs.db')
    #my_db = mysql.connector.connect(
      #host="85.10.205.173",
      #user="orbari123456",
      #passwd="Oliver123",
      #database="music321"
    #)
    # Old database - better keep this !!!
    # host = "85.10.205.173",
    # user = "ori12345",
    # passwd = "Oliver123",
    # database = "musicool123"

    # Old database - better keep this !!!
    # host = "85.10.205.173",
    # user = "orbarilan100",
    # passwd = "R3hab123",
    # database = "music123"
    print(my_db)
    cursor = my_db.cursor()

    cursor.execute("DROP TABLE IF EXISTS genre")
    cursor.execute("DROP TABLE IF EXISTS country")
    cursor.execute("DROP TABLE IF EXISTS city")
    cursor.execute("DROP TABLE IF EXISTS artist")
    cursor.execute("DROP TABLE IF EXISTS concert")
    cursor.execute("DROP TABLE IF EXISTS user")
    cursor.execute("DROP TABLE IF EXISTS location")
    cursor.execute("DROP TABLE IF EXISTS ticket_category")
    cursor.execute("DROP TABLE IF EXISTS concert_ticket")
    cursor.execute("DROP TABLE IF EXISTS concert_artist")
    cursor.execute("DROP TABLE IF EXISTS user")
    cursor.execute("DROP TABLE IF EXISTS user_concert")


    cursor.execute("CREATE TABLE genre (id INT, "
                   "                    name VARCHAR(255) NOT NULL, "                   
                   "                    PRIMARY KEY (id))")

    cursor.execute("CREATE TABLE country (id INT, "
                   "                        name VARCHAR(255) NOT NULL, "                   
                   "                      PRIMARY KEY (id))")

    cursor.execute("CREATE TABLE city (id INT, "
                   "                    name VARCHAR(255) NOT NULL, "
                   "                    country_id INT NOT NULL, "
                   "                    PRIMARY KEY (id),"
                   "                    CONSTRAINT fk_country_city FOREIGN KEY (country_id) "
                   "                    REFERENCES country(id) ON UPDATE CASCADE ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE artist (id INT, "
                   "                        name VARCHAR(255) NOT NULL, "
                   "                        genre_id INT, "                   
                   "                        PRIMARY KEY (id),"
                   "                        CONSTRAINT fk_genre_artist FOREIGN KEY (genre_id) "
                   "                        REFERENCES genre(id) ON UPDATE CASCADE ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE location (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "                        name VARCHAR(255) NOT NULL, "
                   "                        city_id INT NOY NULL,"                   
                   "                        CONSTRAINT fk_location_city FOREIGN KEY (city_id) "
                   "                        REFERENCES city(id) ON UPDATE CASCADE ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE ticket_category (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                                    "name VARCHAR(255) NOT NULL)")

    cursor.execute("CREATE TABLE concert_ticket (concert_id INTEGER NOT NULL,"
                   "                                category_id INTEGER NOT NULL,"
                   "                                price FLOAT NOT NULL,"
                   "                                PRIMARY KEY (concert_id,category_id),"
                   "                                CONSTRAINT fk_concert_ticket_category FOREIGN KEY (category_id) "
                   "                                REFERENCES ticket_category(id) ON UPDATE CASCADE ON DELETE CASCADE,"
                   "                                CONSTRAINT fk_concert_ticket_concert FOREIGN KEY (concert_id) "
                   "                                REFERENCES concert(id) ON UPDATE CASCADE ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE concert_artist (concert_id INTEGER NOT NULL,"
                                                   "artist_id INTEGER NOT NULL,"
                   "                                PRIMARY KEY (concert_id,artist_id),"
                   "                                CONSTRAINT fk_concert_artist_concert FOREIGN KEY (concert_id) "
                   "                                REFERENCES concert(id) ON UPDATE CASCADE ON DELETE CASCADE,"
                   "                                CONSTRAINT fk_concert_artist_artist FOREIGN KEY (artist_id) "
                   "                                REFERENCES artist(id) ON UPDATE CASCADE ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE concert (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   "                        name CHAR(50) NOT NULL, "
                   "                        location_id INT NOT NULL,"
                   "                        start TIMESTAMP NOT NULL,"
                   "                        end TIMESTAMP NOT NULL,"
                   "                        capacity INT NOT NULL,"
           "                                CONSTRAINT fk_location_concert FOREIGN KEY (location_id) REFERENCES location(id) "
                   "                        ON UPDATE CASCADE ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "                    username VARCHAR(255) NOT NULL, "                              
                   "                    password VARCHAR(255) NOT NULL, "                   
                   "                    is_admin BOOLEAN DEFAULT 0,"
                   "                    UNIQUE (username))")

    cursor.execute("CREATE TABLE user_concert (user_id INT NOT NULL, "
                   "                    concert_id INT NOT NULL, "                   
                   "                    PRIMARY KEY (user_id,concert_id), "
                   "                    CONSTRAINT fk_user_concert FOREIGN KEY (concert_id) "
                   "                    REFERENCES concert(id) ON UPDATE CASCADE ON DELETE CASCADE, "
                   "                    CONSTRAINT fk_user_concert_user FOREIGN KEY (user_id) "
                   "                    REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)")

    with open(prefix + 'static/datasets/created/genre.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO genre (name,id) VALUES (?,?)", reader[1:])
        my_db.commit()

    with open(prefix + 'static/datasets/created/country.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO country (name,id) VALUES (?,?)", reader[1:])
        my_db.commit()

    with open(prefix + 'static/datasets/created/city.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO city (name,country_id,id) VALUES (?,?,?)", reader[1:])
        my_db.commit()

    with open(prefix + 'static/datasets/created/artist.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO artist (name,genre_id,id) VALUES (?,?,?)", reader[1:])
        my_db.commit()

    '''
    with open(prefix + 'static/datasets/created/concert.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        for i in range(1, 7500):
            cursor.executemany("INSERT INTO concert (location_id,capacity,name)"
                               " VALUES (?,?,'')", reader[i*50:((i+1)*50)])
            print(i)
            my_db.commit()
    '''

def main():
    mysql_db()


if __name__ == "__main__":
    main()


