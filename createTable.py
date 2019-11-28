import MySQLdb
from dbconnect import connection

db, cursor = connection()

cursor.execute('''drop table if exists  visitor_entry''')
cursor.execute('''drop table if exists  host_entry''')

cursor.execute('''CREATE TABLE host_entry(
    host_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone_no VARCHAR(20),
    password VARCHAR(256))''')

cursor.execute('''CREATE TABLE visitor_entry(
    visitor_id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT,
    FOREIGN KEY(host_id) REFERENCES host_entry(host_id) ON DELETE CASCADE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone_no VARCHAR(20),
    check_in TIMESTAMP DEFAULT 0,
    check_out TIMESTAMP DEFAULT 0)''')
    
db.commit()    
db.close()