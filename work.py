import requests
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
from selenium import webdriver
import os
import zipfile
import re


def unZip(fileName):
    '''
        unzip cert file
    '''
    unzip = zipfile.ZipFile(fileName)
    unzip.extractall("out\\")
    fp = open('out\\signCert.cert')
    text = fp.readline()

    cert_list = find_people_info(text)
    
    cert_list.append(fileName.split("\\")[-1][:-4])

    timeinfo = find_ip(fileName.split("\\")[-1])
    cert_list.append(timeinfo)

    return cert_list

def find_ip(ip):
    #IP정보 비교
    fp =open('ipinfo.txt','r',encoding='UTF8')
    while (True):
        iptime = fp.readline()
        ip_name = iptime.split('\t')[0]

        if (ip_name == ip):
            fp.close()
            return iptime.split('\t')[1]

def get_proxies():
    #외부 IP로 변경을 위한 Proxy 사용
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

def selinumDownload(prox_flag):
    #사이트 정보 다운로드
    url = "[url]"
    ipcheck_url = 'https://httpbin.org/ip'

    i = 4
    while True :
        #Get a proxy from the pool
        if (prox_flag == 1):
        
            try:
                proxies = get_proxies()
                proxy_pool = cycle(proxies)
                proxy = next(proxy_pool)
                if (i>=37000):
                    break
                response = requests.get(ipcheck_url,proxies={"http": proxy, "https": proxy})

                print(response.json())
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--proxy-server=%s' % proxy)

                driver = webdriver.Chrome(options=chrome_options)
                driver.get(url)

                for j in range(i, i+1000):
                    try:
                
                        download_url = '/html/body/table/tbody/tr[' + str(
                            j) + ']/td[2]/a'
                        driver.find_element_by_xpath(download_url).click()
                        i = i+1
                    except :
                        print("end")
                        break
            except:
                print("Skipping. Connnection error")
        else :

            driver = webdriver.Chrome()
            driver.get(url)
            
            while True:
                try :
                    download_url = '/html/body/table/tbody/tr[' + str(
                        i) + ']/td[2]/a'
                    driver.find_element_by_xpath(download_url).click()
                    i = i+1
                except :
                    print("end")


def find_people_info(text):
    #공인인증서 정보 추출	
    '''
        return type
        ['name', '83230778832671167227', 'woori', 'personal', 'yessign', 'country']
    '''
    reg_info = '^cn=([가-힣]+)\(\)([0-z]+),ou=([a-zA-Z]+),ou=([a-zA-Z]+),o=([a-zA-Z]+),c=([a-zA-Z]+)'

    cert_value = re.findall(reg_info, text)


    cert_list =[]

    for i in range(0, len(cert_value[0])):
        cert_list.append(cert_value[0][i])
    print (cert_list)
    exit(1)
    return cert_list

def search(dirname):
    #다운로드 받은 파일 압축 해제 및 DB저장
    sql_insertList =[]
    count = 0
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.zip':

                    cert = unZip(full_filename)
                    sql_insertList.append(cert)
                    count = count + 1

        return 1
    except PermissionError:
        print ("permission Denided")
        return 0
