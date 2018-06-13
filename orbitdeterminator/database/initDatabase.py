"""
This code creates database and tables to each satellite with their md5 hash as table name.

There are 2 codes for database: init_database.py and scraper.py

Important: Run init_database.py before scraper.py

Note: Password field is empty during database connection. Insert password for
      mysql authentication.
"""

import hashlib
import MySQLdb
import requests
from bs4 import BeautifulSoup

def create_database():
    """
    Creating database named "cubesat"

    Args:
        NIL

    Return:
        db : database object
        d : connection flag (0: success)
    """

    db = MySQLdb.connect(host="localhost", user="root", passwd="mysql")
    cursor = db.cursor()
    sql = 'CREATE DATABASE cubesat;'
    cursor.execute(sql)
    # print('Database created')
    d = cursor.execute('use cubesat')
    # print('Database selected')
    # print(d)
    return db, d

def string_to_hash(tle):
    """
    Converts satellite name to its corresponding md5 hexadecimal hash

    Args:
        tle : satellite name

    Return:
        sat_hash : md5 hexadecimal hash
    """

    md5_hash = hashlib.md5(tle.encode())
    sat_hash = md5_hash.hexdigest()
    return sat_hash

def create_tables(db):
    """
    Creating tables in the database

    Args:
        db : database object

    Return:
        NIL
    """
    page = requests.get("https://www.celestrak.com/NORAD/elements/cubesat.txt")
    soup = BeautifulSoup(page.content, 'html.parser')
    tle = list(soup.children)
    tle = tle[0].splitlines()
    cursor = db.cursor()

    sql = 'CREATE TABLE mapping ' + '\
    (sat_name varchar(50), md5_hash varchar(50));'
    cursor.execute(sql)

    success = 0
    error = 0
    for i in range(0, len(tle), 3):
        sat_hash = string_to_hash(tle[i])

        try:
            sql = 'CREATE TABLE ' + str(sat_hash) + '\
            (time varchar(30), line1 varchar(70), line2 varchar(70));'
            cursor.execute(sql)
        except Exception:
            error = error + 1
            print(tle[i] + ' - ' + sat_hash)
        else:
            sql = 'INSERT INTO mapping values(\'%s,\', \'%s\');\
            ' %(str(tle[i]), str(sat_hash))
            cursor.execute(sql)
            db.commit()
            success = success + 1

    print('Tables created : ' + str(success))
    # print('Error/Total : ' + str(error) + '/' + str(error+success))
    db.close()

if __name__ == "__main__":
    db,_ = create_database()
    create_tables(db)
