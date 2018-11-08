# import csv
# import mysql.connector
#
#
# def mysql_db_connection():
#     my_db = mysql.connector.connect(
#       host="85.10.205.173",
#       user="orbarilan10",
#       passwd="Oliver123",
#       database="music10"
#     )
#     print(my_db)
#     cursor = my_db.cursor()
#     cursor.execute("CREATE TABLE IF NOT EXISTS spot (Position VARCHAR(255),Track VARCHAR(255),Artist VARCHAR(255),"
#                    "Streams VARCHAR(255), URL VARCHAR(255),Date VARCHAR(255),Region VARCHAR(255))")
#
#     with open('static/datasets/new.csv', 'r') as f:
#         reader = tuple(csv.reader(f))
#         cursor.executemany('INSERT INTO spot(Position,Track,Artist,Streams,URL,Date,Region)'
#                            ' VALUES (%s,%s,%s,%s,%s,%s,%s)',reader)
#         my_db.commit()