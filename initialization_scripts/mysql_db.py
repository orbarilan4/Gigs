import csv
import mysql.connector

def mysql_db():
    my_db = mysql.connector.connect(
      host="85.10.205.173",
      user="orbarilan100",
      passwd="R3hab123",
      database="music123"
    )
    print(my_db)
    cursor = my_db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS genre (genre_name VARCHAR(255) NOT NULL, "
                   "genre_id INT, PRIMARY KEY (genre_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS city (city_name VARCHAR(255) NOT NULL, "
                   "city_id INT, PRIMARY KEY (city_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS country (country_name VARCHAR(255) NOT NULL, "
                   "country_id INT, PRIMARY KEY (country_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS artist (artist_name VARCHAR(255) NOT NULL, "
                   "genre_id INT, artist_id INT, PRIMARY KEY (artist_id),CONSTRAINT fk_genre_id FOREIGN KEY (genre_id) "
                   "REFERENCES genre(genre_id) ON UPDATE CASCADE ON DELETE RESTRICT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS concert (artist_id INT,city_id INT,country_id INT, "
                   "date_time VARCHAR(255),price INT,age_limit INT,capacity INT,"
                   "CONSTRAINT fk_artist_id FOREIGN KEY (artist_id) REFERENCES artist(artist_id) "
                   "ON UPDATE CASCADE ON DELETE RESTRICT,"
                   "CONSTRAINT fk_city_id FOREIGN KEY (city_id) REFERENCES city(city_id) "
                   "ON UPDATE CASCADE ON DELETE RESTRICT,"
                   "CONSTRAINT fk_country_id FOREIGN KEY (country_id) REFERENCES country(country_id) "
                   "ON UPDATE CASCADE ON DELETE RESTRICT,"
                   "PRIMARY KEY (artist_id,date_time))")

    with open('../static/datasets/created/genre.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO genre (genre_name,genre_id) VALUES (%s,%s)", reader[1:])
        my_db.commit()

    with open('../static/datasets/created/city.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO city (city_name,city_id) VALUES (%s,%s)", reader[1:])
        my_db.commit()

    with open('../static/datasets/created/country.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO country (country_name,country_id) VALUES (%s,%s)", reader[1:])
        my_db.commit()

    with open('../static/datasets/created/artist.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        cursor.executemany("INSERT INTO artist (artist_name,genre_id,artist_id) VALUES (%s,%s,%s)", reader[1:])
        my_db.commit()

    with open('../static/datasets/created/concert.csv', 'r', encoding="utf8") as f:
        reader = tuple(csv.reader(f))
        for i in range(1, 7500):
            cursor.executemany("INSERT INTO concert (artist_id,city_id,country_id,date_time,price,age_limit,capacity)"
                               " VALUES (%s,%s,%s,%s,%s,%s,%s)", reader[i*50:((i+1)*50)])
            print(i)
            my_db.commit()



def main():
    mysql_db()


if __name__ == "__main__":
    main()
