import sqlite3, datetime


def get_daily_info():

    conn = sqlite3.connect('bandwidth_jalali.db')
    cur = conn.cursor()
    cur.execute("ATTACH DATABASE 'bandwidth_jalali.db' as jalali;")
   
    data =cur.execute("select * from jalali;")
    dates = []
    RX = []
    TX = []

    for i in data:
        dates.append(i[0])
        RX.append(i[1])
        TX.append(i[2])

    return(dates, RX, TX)

