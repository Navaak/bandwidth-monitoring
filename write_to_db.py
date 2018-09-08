import sqlite3
import convert_to_jalali

conn_module = convert_to_jalali.create_connection('bandwidth.db')
data = convert_to_jalali.convert_dates(conn_module)

conn = sqlite3.connect('bandwidth_jalali.db')

cur = conn.cursor()

cur.execute('''CREATE TABLE jalali
             (date text, RX real, TX real)''')

for item in data:
    cur.execute("INSERT INTO jalali VALUES ('{0}',{1},{2})".format(item[0], item[1], item[2]))
    conn.commit()

conn.close()


