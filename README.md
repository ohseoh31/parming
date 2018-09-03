# parming


1. selenium을 사용한 웹페이지 접근 및 파일 다운로드
```
수많은 파일을 다운로드하는경우 urlopen, urllib 사용하는것이 효율적임
```
</br>

2. Whois open API 사용 
```
https://xn--c79as89aj0e29b77z.xn--3e0b707e/kor/whois/openAPI_KeyCre.jsp
```
</br>

3. mysql DB to csv file

> SHOW VARIABLES LIKE "secure_file_priv";

```
SELECT * FROM [table Name]
INTO OUTFILE 'my_table.csv'
CHARACTER SET euckr
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '\\'
LINES TERMINATED BY '\n' ;
```
