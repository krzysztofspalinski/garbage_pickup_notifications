#!/usr/bin/env python3

import requests
import json
import mysql.connector

headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

with open('address_conf.txt') as f:
	address_id = str(f.read())

form_data = {
	'_portalCKMjunkschedules_WAR_portalCKMjunkschedulesportlet_INSTANCE_o5AIb2mimbRJ_addressPointId': address_id
}

data_raw = None

with requests.Session() as sess:
	url = 'https://warszawa19115.pl/harmonogramy-wywozu-odpadow?p_p_id=portalCKMjunkschedules_WAR_portalCKMjunkschedulesportlet_INSTANCE_o5AIb2mimbRJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=ajaxResourceURL&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1'
	req = sess.post(url, data=form_data, headers=headers)
	data_raw = str(req.content)

data = data_raw
data = data[3:-2]
data = data.replace('\\', '')
data = data.replace('"bio - gastronomia/targowiska"', 'GT')
data = data.replace('"bio"', 'BK')
data = data.replace('"metale i tworzywa sztuczne"', 'BK')
data = data.replace('"papier"', 'BK')
data = data.replace('"szkxc5x82o"', 'BK')
data = data.replace('"odpady zielone"', 'BK')
data = data.replace('"odpady wielkogabarytowe" jako', 'BK')
data = data.replace('"odpady zmieszane"', 'BK')

parsed_json = (json.loads(data))


pickup_date_BIO = parsed_json['harmonogramy'][1]['data']
pickup_date_PLA = parsed_json['harmonogramy'][2]['data']
pickup_date_PAP = parsed_json['harmonogramy'][3]['data']
pickup_date_SZK = parsed_json['harmonogramy'][4]['data']
pickup_date_ZIE = parsed_json['harmonogramy'][5]['data']
pickup_date_GAB = parsed_json['harmonogramy'][6]['data']
pickup_date_ZMI = parsed_json['harmonogramy'][7]['data']


with open("db_conf.txt", 'r') as f:
	host = f.readline().rstrip('\n')
	user = f.readline().rstrip('\n')
	passwd_db = f.readline().rstrip('\n')
	database = f.readline().rstrip('\n')


mydb = mysql.connector.connect(
  host=host,
  user=user,
  passwd=passwd_db,
  database=database)

mycursor = mydb.cursor()


create_table = 'CREATE TABLE garbage_pickup_dates (date DATE, garbage_type VARCHAR(3), PRIMARY KEY (date, garbage_type))'
try:
	mycursor.execute(create_table)
except:
	pass

sql = "INSERT INTO garbage_pickup_dates (date, garbage_type) VALUES (%s, %s)"

try:
	val = (pickup_date_BIO, "BIO")
	mycursor.execute(sql, val)
except:
	pass
try:
	val = (pickup_date_PLA, "PLA")
	mycursor.execute(sql, val)
except:
	pass
try:
	val = (pickup_date_PAP, "PAP")
	mycursor.execute(sql, val)
except:
	pass
try:
	val = (pickup_date_SZK, "SZK")
	mycursor.execute(sql, val)
except:
	pass
try:
	val = (pickup_date_ZIE, "ZIE")
	mycursor.execute(sql, val)
except:
	pass
try:
	val = (pickup_date_GAB, "GAB")
	mycursor.execute(sql, val)
except:
	pass
try:
	val = (pickup_date_ZMI, "ZMI")
	mycursor.execute(sql, val)
except:
	pass

mydb.commit()
mycursor.close()
mydb.close()


