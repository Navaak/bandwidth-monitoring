import sqlite3

conn = sqlite3.connect('bandwidth_jalali.db')

cur = conn.cursor()

cur.execute("ATTACH DATABASE 'bandwidth_jalali.db' as jalali;")
cur.execute("select * from jalali;")
data = cur.fetchall()


for item in data:
    j_date = (str(item[0]))
    day_of_month = j_date[8:10]



conn.commit()
conn.close()