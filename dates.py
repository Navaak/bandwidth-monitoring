import sqlite3
from sqlite3 import Error
import jdatetime

def create_connection(db_file):

    try:
        conn = sqlite3.connect(db_file)
        return conn

    except Error as e:
        print(e)


    return None



def select(conn):

    cur = conn.cursor()
    cur.execute("select * from daily;")

    rows = cur.fetchall()

    for row in rows:
    
        year = int(row[0][0:4])
        
        if row[0][5:6] == int(0) :         
            month = int(row[0][6:7])

        else:
            month = int(row[0][5:7])

        day = int(row[0][8:10])

        date = jdatetime.date.fromgregorian(day=day, month=month, year=year)

        print(date)


conn = create_connection('bandwidth.db')
select(conn)