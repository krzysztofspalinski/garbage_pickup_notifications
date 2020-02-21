#!/usr/bin/env python3

import smtplib, ssl
import mysql.connector
import datetime


def parse_emails(receiver_email: dict):
	recepients = str(receiver_email)
	recepients = recepients.replace('\'', '')
	recepients = recepients.replace('[', '')
	recepients = recepients.replace(']', '')


tommorow_date = str(datetime.date.today() + datetime.timedelta(days = 1))
garbage_types = {'BIO': 'BIO', 'PLA': 'PLASTIK', 'PAP': 'PAPIER', 'SZK': 'SZKLO', 'ZIE': 'ZIELONE','GAB': 'GABARYTY', 'ZMI': 'ZMIESZANE'}



with open("db_conf.txt") as f:
	host = f.readline().rstrip('\n')
	user = f.readline().rstrip('\n')
	passwd_db = f.readline().rstrip('\n')
	database = f.readline().rstrip('\n')


port = 465
context = ssl.create_default_context()
with open("mail_conf.txt", 'r') as f:
	receiver_email = f.read().splitlines()
mail_host = receiver_email.pop(0)
sender_email = receiver_email.pop(0)


mydb = mysql.connector.connect(
  host=host,
  user=user,
  passwd=passwd_db,
  database=database)

mycursor = mydb.cursor()

sql_print_tommorow_garbage = f'SELECT garbage_type FROM garbage_pickup_dates WHERE date=\'{tommorow_date}\''
mycursor.execute(sql_print_tommorow_garbage)
myresult = mycursor.fetchall()
for x in myresult:
	garbage_type = str(x)[2:5]
	garbage_name = garbage_types[garbage_type]

	message = f'''\
From: [WYWOZ SMIECI] <{sender_email}>
To: {receiver_email}
Subject: Jutro ({tommorow_date}) wywozone sa smieci {garbage_name}

Jutro ({tommorow_date}) wywozone sa smieci {garbage_name}.
Wiadomosc wyslana automatycznie. Prosze na nia nie odpowiadac.'''

	with smtplib.SMTP_SSL(mail_host, port, context=context) as server:
		server.login(sender_email, passwd_db)
		server.sendmail(sender_email, receiver_email, message)

mydb.commit()
mycursor.close()
mydb.close()