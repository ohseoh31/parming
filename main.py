from selenium import webdriver
import os
import zipfile
import re
import parming.dbquery


'''
서버 (http://107.174.85.141/cert)
1. 피해자의 일련번호 - 피해시각(서버에 피해자의 공인인증서가 업로드된 시간)
- 국가코드

- 피해자의 이름
- 은행명
- 계좌번호
- IP주소
'''


'''
val_at = re.findall(find_value_at, text)

            if val != [] and val_at == []:
                count +=1
                self.val_List.append([count, val[0][0].upper(), val[0][1].upper()])
'''





def unZip(fileName):
    #print("fileName %s" % (fileName))
    unzip = zipfile.ZipFile(fileName)

    # cert_list = []

    # print (fileName)
    # print ()
    unzip.extractall("out\\")

    fp = open('out\\signCert.cert')
    text = fp.readline()

    # print(text)
    cert_list = find_people_info(text)
    cert_list.append(fileName.split("\\")[2][:-4])

    timeinfo = find_ip(fileName.split("\\")[2])
    cert_list.append(timeinfo)


    #os.system("del .\\out\\signCert.cert")
    return cert_list
    #print('unzip')
#
# /html/body/table/fileName.split("\\")[2][:-3]tbody/tr[4]/td[2]/a
# /html/body/table/tbody/tr[5]/td[2]/a
# /html/body/table/tbody/tr[6]/td[2]/a


def find_ip(ip):
    fp =open('ipinfo.txt','r')

    while (True):
        iptime = fp.readline()
        #print (iptime)
        #print (iptime.split('\t'))
        ip_name = iptime.split('\t')[0]
        if (ip_name == ip):
            fp.close()

            return iptime.split('\t')[1]


def selinumDownload():
    driver = webdriver.Chrome()
    driver.get("http://107.174.85.141/cert/")

    i = 4
    while True:
        try:
            download_url = '/html/body/table/tbody/tr[' + str(
                i) + ']/td[2]/a'
            driver.find_element_by_xpath(download_url).click()
            i = i+1
        except :
            print("end")




#공인인증서 정보 추출
def find_people_info(text):
    #print (text)
    reg_info = '^cn=([가-힣]+)\(\)([0-z]+),ou=([a-zA-Z]+),ou=([a-zA-Z]+),o=([a-zA-Z]+),c=([a-zA-Z]+)'

    cert_value = re.findall(reg_info, text)

    '''
        def findIP_time(fileName(ip정보))
        return type
        ip data
        date data
    '''
    #Name 계좌번호
    cert_list =[]

    for i in range(0, len(cert_value[0])):
        cert_list.append(cert_value[0][i])

    # print (cert_list)
    return cert_list
    #sql_list.append()


def search(dirname):
    sql_insertList =[]
    count = 0
    try:
        filenames = os.listdir(dirname)
        #print (len(filenames))
        #zzzexit(1)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.zip':

                    #unzip file
                    cert = unZip(full_filename)
                    sql_insertList.append(cert)
                    count = count + 1
                    if len(sql_insertList) >= 2000 or count >= len(filenames):
                        # print (sql_insertList)
                        parming.dbquery.inputDB(sql_insertList)
                        sql_insertList = []

    except PermissionError:
        print ("permission Denided")
        pass


if __name__ == "__main__":
    '''
        using selinum download zip file
    '''
    selinumDownload()


    '''
         copy Download/ipfiles to .\\files
    '''
    dirname = ".\\files"
    #dirname = "C:\\Users\\ohseo\\Downloads\\files

    '''
         unzip and insert data into database
    '''
    search(dirname)

    '''
        insert into database ipInfo
    '''
    parming.dbquery.inputIPDB()











'''
    fileName = 'signCert.cert'
    sql_list = []

    cert_list = find_people_info(fileName)

    sql_list.append(cert_list)
    inputDB(sql_list)
'''


