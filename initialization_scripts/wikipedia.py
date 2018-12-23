import csv
import sqlite3

def mysql_db():
    conn = sqlite3.connect('../db/wiki.db')


    qry = open('../static/datasets/wiki/images.sql', 'r', encoding="utf8", errors='ignore').read()

    c = conn.cursor()
    c.executescript(qry)
    conn.commit()
    c.close()
    conn.close()


def main():
    mysql_db()


if __name__ == "__main__":
    main()


