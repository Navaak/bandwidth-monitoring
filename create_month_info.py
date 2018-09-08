import sqlite3
import jdatetime


month_list = []

def get_month_info_from_daily_info():

    today = jdatetime.date.today()
    today = str(today)

    conn = sqlite3.connect('bandwidth_jalali.db')
    cur = conn.cursor()
    cur.execute("ATTACH DATABASE 'bandwidth_jalali.db' as jalali;")


    for year in range(1395, 1398):
        for month in range(01 , 10):
            x = "(date > '{0}-0{1}-01' and date <= '{0}-0{1}-31');".format(year, month)
            query = "select sum(rx), sum(tx) from jalali where {0}".format(x)

            cur.execute(query)
            data = cur.fetchall()

            date = str(year)+"-"+str(month)
            month_data = (date, data)
            month_list.append(month_data)
    
            
        for month in range(10, 13):
            x = "(date > '{0}-{1}-01' and date <= '{0}-{1}-31');".format(year, month)
            query = "select sum(rx), sum(tx) from jalali where {0}".format(x)

            cur.execute(query)
            data = cur.fetchall()

            date = str(year)+"-"+str(month)            
            month_data = (date, data)
            month_list.append(month_data)
    
    return month_list
   
    conn.commit()
    conn.close()



def month_info():
    
    dates = []
    RX    = []
    TX    = []
    
    data = get_month_info_from_daily_info()
   
    for item in data:
        dates.append(item[0])
        RX.append(item[1][0][0])
        TX.append(item[1][0][1])

    return(dates, RX, TX)


