import sqlite3, jdatetime
from sqlite3 import Error


def create_connection(db_file):

    try:
        conn = sqlite3.connect(db_file)
        return conn

    except Error as e:
        print(e)

    return None



def convert_dates(conn):
  
    jalali_list = []

    cur = conn.cursor()
    cur.execute("ATTACH DATABASE 'bandwidth.db' as daily;")
    cur.execute("select * from daily;")

    rows = cur.fetchall()
  
    for row in rows:

        year = int(row[0][0:4])
        
        if row[0][5:6] == int(0) :         
            month = int(row[0][6:7])

        else:
            month = int(row[0][5:7])

        day = int(row[0][8:10])

        RX = row[1]
        TX = row[2]

        date = jdatetime.date.fromgregorian(day=day, month=month, year=year)
        jalali_list.append((str(date), RX, TX))
   
    return(jalali_list)


# Write jalali info into database
conn_module = create_connection('bandwidth.db')
data = convert_dates(conn_module)
conn = sqlite3.connect('bandwidth_jalali.db')

cur = conn.cursor()

cur.execute('''CREATE TABLE jalali
            (date text, RX real, TX real)''')

for item in data:
    cur.execute("INSERT INTO jalali VALUES ('{0}',{1},{2})".format(item[0], item[1], item[2]))
    conn.commit()

conn.close()

