import MySQLdb
from setup import DATABASE_HOST, DATABASE_NAME, DB_USER, DB_PASSWORD
def connection():
    db = MySQLdb.connect(host = DATABASE_HOST,
                           user = DB_USER,
                           passwd = DB_PASSWORD,
                           db = DATABASE_NAME)
    cursor = db.cursor()
    return db,cursor