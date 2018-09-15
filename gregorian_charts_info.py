import sqlite3, datetime

def get_daily_info():

    conn = sqlite3.connect('bandwidth.db')
    cur = conn.cursor()
    cur.execute("ATTACH DATABASE 'bandwidth.db' as daily;")
   
    data  = cur.execute("select * from daily;")
    dates = []
    RX    = []
    TX    = []

    for i in data:
        dates.append(i[0])
        RX.append(i[1])
        TX.append(i[2])

    return(dates, RX, TX)




def get_month_info_from_daily_info():
    
    today = datetime.datetime.today()
    today = str(today)
    current_year = int(str(today)[0:4])
    print(current_year)
    

    month_list = [] 
    
    conn = sqlite3.connect('bandwidth.db')
    cur  = conn.cursor()
    cur.execute("ATTACH DATABASE 'bandwidth.db' as daily;")

    for year in range(2016, current_year+1):
        for month in range(1 , 10):
            x = "(day_of_year > '{0}-0{1}-01' and day_of_year <= '{0}-0{1}-31');".format(year, month)
            query = "select sum(rx), sum(tx) from daily where {0}".format(x)

            cur.execute(query)
            data = cur.fetchall()

            date = str(year)+"-"+str(month)
            month_data = (date, data)
            month_list.append(month_data)
    
            
        for month in range(10, 13):
            tmp_date = "(day_of_year > '{0}-{1}-01' and day_of_year <= '{0}-{1}-31');".format(year, month)
            query = "select sum(rx), sum(tx) from daily where {0}".format(tmp_date)

            cur.execute(query)
            data = cur.fetchall()

            date = str(year)+"-"+str(month)            
            month_data = (date, data)
            month_list.append(month_data)
    
    return month_list
    
    conn.commit()
    conn.close()


def month_info():
    
    data  = []
    dates = []
    RX    = []
    TX    = []

    data = get_month_info_from_daily_info()
   
    for item in data:
        dates.append(item[0])
        RX.append(item[1][0][0])
        TX.append(item[1][0][1])

    return(dates, RX, TX)

