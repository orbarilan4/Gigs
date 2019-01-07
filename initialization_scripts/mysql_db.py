import csv,mysql.connector
#import sqlite3

def mysql_db():
    prefix = ''
    # try:
    #     my_db = sqlite3.connect('db/gigs.db')
    # except:
    prefix = '../'
    #     my_db = sqlite3.connect(prefix + 'db/gigs.db')
    my_db = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="1q2w3e4r"
    )
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

    cursor.execute("CREATE DATABASE IF NOT EXISTS music321;")
    cursor.execute("USE music321;")

    cursor.execute("DROP TABLE IF EXISTS concert_artist")
    cursor.execute("DROP TABLE IF EXISTS artist")
    cursor.execute("DROP TABLE IF EXISTS genre")
    cursor.execute("DROP TABLE IF EXISTS concert_ticket")
    cursor.execute("DROP TABLE IF EXISTS user_concert")
    cursor.execute("DROP TABLE IF EXISTS concert")
    cursor.execute("DROP TABLE IF EXISTS location")
    cursor.execute("DROP TABLE IF EXISTS city")
    cursor.execute("DROP TABLE IF EXISTS country")
    cursor.execute("DROP TABLE IF EXISTS user")
    cursor.execute("DROP TABLE IF EXISTS ticket_category")
    cursor.execute("DROP TABLE IF EXISTS user")



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

    cursor.execute("CREATE TABLE location (id INTEGER PRIMARY KEY AUTO_INCREMENT,"
                   "                        name VARCHAR(255) NOT NULL, "
                   "                        city_id INT NOT NULL,"                   
                   "                        CONSTRAINT fk_location_city FOREIGN KEY (city_id) "
                   "                        REFERENCES city(id) ON UPDATE CASCADE ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE ticket_category (id INTEGER PRIMARY KEY AUTO_INCREMENT,"
                                                    "name VARCHAR(255) NOT NULL)")

    cursor.execute("CREATE TABLE concert (id INTEGER PRIMARY KEY AUTO_INCREMENT, "
                   "                        name CHAR(100) NOT NULL, "
                   "                        location_id INT NOT NULL,"
                   "                        start TIMESTAMP NOT NULL,"
                   "                        end TIMESTAMP NOT NULL,"
                   "                        capacity INT NOT NULL,"
           "                                CONSTRAINT fk_location_concert FOREIGN KEY (location_id) REFERENCES location(id) "
                   "                        ON UPDATE CASCADE ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE concert_ticket (concert_id INTEGER NOT NULL,"
                   "                                category_id INTEGER NOT NULL,"
                   "                                price FLOAT NOT NULL,"
                   "                                PRIMARY KEY (concert_id,category_id),"
                   "                                CONSTRAINT fk_concert_ticket_category FOREIGN KEY (category_id) "
                   "                                REFERENCES ticket_category(id) ON UPDATE CASCADE ON DELETE CASCADE,"
                   "                                CONSTRAINT fk_concert_ticket_concert FOREIGN KEY (concert_id) "
                   "                                REFERENCES concert(id) ON UPDATE CASCADE ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE concert_artist  (concert_id INTEGER NOT NULL,"
                                                   "artist_id INTEGER NOT NULL,"
                   "                                PRIMARY KEY (concert_id,artist_id),"
                   "                                CONSTRAINT fk_concert_artist_concert FOREIGN KEY (concert_id) "
                   "                                REFERENCES concert(id) ON UPDATE CASCADE ON DELETE CASCADE,"
                   "                                CONSTRAINT fk_concert_artist_artist FOREIGN KEY (artist_id) "
                   "                                REFERENCES artist(id) ON UPDATE CASCADE ON DELETE CASCADE)")



    cursor.execute("CREATE TABLE user (id INTEGER PRIMARY KEY AUTO_INCREMENT,"
                   "                    username VARCHAR(255) NOT NULL, "                              
                   "                    password VARCHAR(255) NOT NULL, "                   
                   "                    is_admin BOOLEAN DEFAULT 0,"
                   "                    UNIQUE (username))")

    cursor.execute("CREATE TABLE user_concert (user_id INT NOT NULL, "
                   "                    like_concert BOOLEAN DEFAULT 0,"
                   "                    quantity INT NOT NULL, " 
                   "                    concert_id INT NOT NULL, "                   
                   "                    PRIMARY KEY (user_id,concert_id), "
                   "                    CONSTRAINT fk_user_concert FOREIGN KEY (concert_id) "
                   "                    REFERENCES concert(id) ON UPDATE CASCADE ON DELETE CASCADE, "
                   "                    CONSTRAINT fk_user_concert_user FOREIGN KEY (user_id) "
                   "                    REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)")

    with open(prefix + 'static/datasets/created/genre.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO genre (name,id) VALUES (%s,%s)", reader[1:])
        my_db.commit()

    with open(prefix + 'static/datasets/created/country.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO country (name,id) VALUES (%s,%s)", reader[1:])
        my_db.commit()

    with open(prefix + 'static/datasets/created/city.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO city (name,country_id,id) VALUES (%s,%s,%s)", reader[1:])
        my_db.commit()

    with open(prefix + 'static/datasets/created/artist.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO artist (name,genre_id,id) VALUES (%s,%s,%s)", reader[1:])
        my_db.commit()

    with open(prefix + 'static/datasets/created/location.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO location (id,name,city_id) VALUES (%s,%s,%s)", reader[1:])
        my_db.commit()

    with open(prefix + 'static/datasets/created/users.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO user (id,username,password,is_admin) VALUES (%s,%s,%s,%s)", reader[1:])
        my_db.commit()

    with open(prefix + 'static/datasets/created/concert.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO concert (id,name,location_id,start,end,capacity) VALUES (%s,%s,%s,%s,%s,%s)", reader[1:])
        my_db.commit()

    with open(prefix + 'static/datasets/created/artist_concert.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO concert_artist (concert_id,artist_id) VALUES (%s,%s)", reader[1:])
        my_db.commit()
    with open(prefix + 'static/datasets/created/ticket_category.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO ticket_category (id,name) VALUES (%s,%s)", reader[1:])
        my_db.commit()

    with open(prefix + 'static/datasets/created/concert_ticket.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO concert_ticket (concert_id,category_id,price) VALUES (%s,%s,%s)", reader[1:])
        my_db.commit()

    with open(prefix + 'static/datasets/created/user_concert.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO user_concert (user_id,like_concert,quantity,concert_id) VALUES (%s,%s,%s,%s)", reader[1:])
        my_db.commit()






    '''
    with open(prefix + 'static/datasets/created/concert.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        for i in range(1, 7500):
            cursor.executemany("INSERT INTO concert (location_id,capacity,name)"
                               " VALUES (%s,%s,'')", reader[i*50:((i+1)*50)])
            print(i)
            my_db.commit()
    '''

def main():
    mysql_db()


if __name__ == "__main__":
    main()


