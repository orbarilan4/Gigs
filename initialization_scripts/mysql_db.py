import csv
import sqlite3

def mysql_db():
    my_db = sqlite3.connect('db/gigs.db')
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
    cursor.execute("DROP TABLE IF EXISTS user_concert")


    cursor.execute("CREATE TABLE genre (genre_name VARCHAR(255) NOT NULL, "
                   "genre_id INT, PRIMARY KEY (genre_id))")
    cursor.execute("CREATE TABLE country (country_name VARCHAR(255) NOT NULL, "
                   "country_id INT, PRIMARY KEY (country_id))")
    cursor.execute("CREATE TABLE city (city_name VARCHAR(255) NOT NULL, "
                   "country_id INT, city_id INT, PRIMARY KEY (city_id),CONSTRAINT fk_country_id FOREIGN KEY (country_id) "
                   "REFERENCES country(country_id) ON UPDATE CASCADE ON DELETE RESTRICT)")
    cursor.execute("CREATE TABLE artist (artist_name VARCHAR(255) NOT NULL, "
                   "genre_id INT, artist_id INT, PRIMARY KEY (artist_id),CONSTRAINT fk_genre_id FOREIGN KEY (genre_id) "
                   "REFERENCES genre(genre_id) ON UPDATE CASCADE ON DELETE RESTRICT)")
    cursor.execute("CREATE TABLE concert (id INT PRIMARY KEY,"
                                                        "name CHAR(50) NOT NULL,"
                                                        "artist_id INT,"
                                                        "city_id INT, "
                                                        "date_time TIMESTAMP,"
                                                        "price INT,"
                                                        "age_limit INT,"
                                                        "capacity INT,"                   
                   "CONSTRAINT fk_artist_id FOREIGN KEY (artist_id) REFERENCES artist(artist_id) "
                   "ON UPDATE CASCADE ON DELETE RESTRICT,"
                   "CONSTRAINT fk_city_id FOREIGN KEY (city_id) REFERENCES city(city_id) "
                   "ON UPDATE CASCADE ON DELETE RESTRICT)")
    cursor.execute("CREATE TABLE user (username VARCHAR(255) NOT NULL, age INT, city_id INT, "
                   "password VARCHAR(255) NOT NULL, picture VARCHAR(10000) NOT NULL, "
                   "is_admin BOOLEAN, PRIMARY KEY (username), "
                   "CONSTRAINT fk_user_city_id FOREIGN KEY (city_id) REFERENCES city(city_id) "
                   "ON UPDATE CASCADE ON DELETE RESTRICT)")
    cursor.execute("CREATE TABLE user_concert (username VARCHAR(255) NOT NULL, concert_id INT, "
                   "date_time TIMESTAMP, PRIMARY KEY (username,concert_id), "
                   "CONSTRAINT fk_user_concert_id_datetime FOREIGN KEY (concert_id) "
                   "REFERENCES concert(id) ON UPDATE CASCADE ON DELETE RESTRICT, "
                   "CONSTRAINT fk_user_concert_username FOREIGN KEY (username) "
                   "REFERENCES user(username) ON UPDATE CASCADE ON DELETE RESTRICT)")

    with open('static/datasets/created/genre.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO genre (genre_name,genre_id) VALUES (?,?)", reader[1:])
        my_db.commit()

    with open('static/datasets/created/country.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO country (country_name,country_id) VALUES (?,?)", reader[1:])
        my_db.commit()

    with open('static/datasets/created/city.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO city (city_name,country_id,city_id) VALUES (?,?,?)", reader[1:])
        my_db.commit()

    with open('static/datasets/created/artist.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO artist (artist_name,genre_id,artist_id) VALUES (?,?,?)", reader[1:])
        my_db.commit()

    with open('static/datasets/created/concert.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        for i in range(1, 7500):
            cursor.executemany("INSERT INTO concert (artist_id,city_id,date_time,price,age_limit,capacity,name,id)"
                               " VALUES (?,?,?,?,?,?,'',NULL)", reader[i*50:((i+1)*50)])
            print(i)
            my_db.commit()


def main():
    mysql_db()


if __name__ == "__main__":
    main()


