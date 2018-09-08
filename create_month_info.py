import sqlite3
import jdatetime


today = jdatetime.date.today()
today = str(today)

conn = sqlite3.connect('bandwidth_jalali.db')
cur = conn.cursor()
cur.execute("ATTACH DATABASE 'bandwidth_jalali.db' as jalali;")

month_list = []

def month_info():
    for year in range(1395, 1398):
        for month in range(01 , 10):
            x = "(date > '{0}-0{1}-01' and date <= '{0}-0{1}-31');".format(year, month)
            query = "select sum(rx), sum(tx) from jalali where {0}".format(x)
            #print("======>", query)

            cur.execute(query)
            data = cur.fetchall()
            month_data = (year,month, data)
            month_list.append(month_data)
            #return(year, month , data)
            


            
        for month in range(10, 13):
            x = "(date > '{0}-{1}-01' and date <= '{0}-{1}-31');".format(year, month)
            query = "select sum(rx), sum(tx) from jalali where {0}".format(x)
            #print("======>", query)


            cur.execute(query)
            data = cur.fetchall()
            month_data = (year, month, data)
            month_list.append(month_data)
            #return(year, month , data)
    return month_list
    conn.commit()
    conn.close()


x = month_info()
print(x)