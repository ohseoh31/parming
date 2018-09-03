import pymysql
import re
import requests
import json

def inputDB(sql_list) : #insert log file into mysql database
    conn = pymysql.connect(host='localhost', user='root', password='1234',
                           db='cert_info', charset='utf8')

    curs = conn.cursor()
    sql = """insert into cert(date, name, account_number, bank_info,  country, IP) values (%s, %s, %s, %s, %s, %s )"""

    for i in range(0, len(sql_list)):

        #date, bank_info, accountnumber, ip, country
        curs.execute(sql, (sql_list[i][7][:-2], sql_list[i][0], sql_list[i][1], sql_list[i][2], sql_list[i][5],sql_list[i][6]))
        #curs.execute(sql, ('2018-08-26', 'name', 1, 'kr', 'ip'))
    print("dataBase Insert")
    conn.commit()





def getCountry(ip_info):
    api_key = '2018083111331754935052'

    url = 'http://whois.kisa.or.kr/openapi/ipascc.jsp?query=' + ip_info + '&key=' + api_key + '&answer=json'
    # url = 'http://whois.kisa.or.kr/openapi/ipascc.jsp?query=211.101.23.45&key=2018083111331754935052&answer=json'
    req = requests.get(url)
    text = req.text

    data = json.loads(text)
    return data["whois"]["countryCode"]


def retIPList(iptime):
    iplist = []
    country = getCountry(iptime.split('\t')[0][:-4])

    iplist.append(iptime.split('\t')[0][:-4])
    iplist.append(iptime.split('\t')[1][:-1])
    iplist.append(country)
    return iplist

def inputIPDB():
    fp = open('ipinfo.txt', 'r')

    conn = pymysql.connect(host='localhost', user='root', password='1234',
                           db='cert_info', charset='utf8')
    sql = """insert into ip_info(ip_addr, date, country) values (%s, %s, %s)"""
    curs = conn.cursor()
    input_IPdbList = []
    count = 0
    while (True):
        iptime = fp.readline()

        count = count + 1

        if (len(input_IPdbList) >= 3000 or iptime==''):
            for i in range(0, len(input_IPdbList)):
                curs.execute(sql, (input_IPdbList[i][0], input_IPdbList[i][1], input_IPdbList[i][2]))

            input_IPdbList = []
            print ('input db')
            conn.commit()
            if (iptime == ''):
                break
        ipList = retIPList(iptime)
        input_IPdbList.append(ipList)