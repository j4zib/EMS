import MySQLdb

def connection():
    db = MySQLdb.connect(host="localhost",
                           user = "timetable",
                           passwd = "12345",
                           db = "time_table")
    cursor = db.cursor()
    return db,cursor