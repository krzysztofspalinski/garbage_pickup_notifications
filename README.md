### Scripts for sending email notifications for garbage pickup

`scrapper.py` is used to get the next pickup dates for different types of trash (glass, paper, bio, etc.) from the website and upload them to the database.

`sender.py` is used to check in the database if there is any kind of garbage picked up the next day. If there is a record in the database for pickup, then email is sent with information on what type of trash is picked up. 