################################################################################
# Copyright (Python) taegyu <https://github.com/ohseoh31>                      #
# @author taegue (ohseoh31@github.com) bob7 df                                 #
# @brief  youtube mp4 file download code with python                           #
# using command : python3 -p 1 or 0                                            #
#                 python3 -i "unzip_folder_path" [--input="unzip_folder_path"] #
################################################################################
import sys
import getopt
import dbquery
import work




# help alert
def help():
    print ("print help usage")
    print ("[-p] is proxy option and download cert")
    print ("    use proxy 1")
    print ("    None use proxy 0")
    print ("[-i][--input] is input cert info insert databse path")
    print ("[-h][--help] is help option")
    return 
 
def noOption():
    print ('print help usage')
    print ('[-h][--help] command input')


def main():
    try:
    # 여기서 입력을 인자를 받는 파라미터는 단일문자일 경우 ':' 긴문자일경우 '='을끝에 붙여주면됨
        opts, args = getopt.getopt(sys.argv[1:],"p:i:",["input=","help"])
    
    except getopt.GetoptError as err:
        print (str(err))
        help()
        sys.exit(1)

    proxy_option = 0
    cert_path = None
    
    if opts == [] :
        #noOption()
        help()
        sys.exit(1)

    for opt,arg in opts:

        if (opt == '-p'):
            '''
                using selinum download zip file
            '''
            proxy_option = arg
            work.selinumDownload(proxy_option)
            sys.exit(1)
        elif (opt == '-i' or opt =='--input'):
            cert_path = arg
            '''
                unzip and insert data into database
            '''
            work.search(cert_path)
            dbquery.inputIPDB()
            sys.exit(1)
        elif ( opt == "-h") or ( opt == "--help"):
            help()
            sys.exit(1)


if __name__ == "__main__":
    '''
        using selinum download zip file
    '''
    main()

  











'''
    fileName = 'signCert.cert'
    sql_list = []

    cert_list = find_people_info(fileName)

    sql_list.append(cert_list)
    inputDB(sql_list)
'''


