from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
import json
import urllib3

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

cursor = mysql.connection.cursor()
 
#Executing SQL Statements
cursor.execute(''' CREATE TABLE table_name(field1, field2...) ''')
cursor.execute(''' INSERT INTO table_name VALUES(v1,v2...) ''')
cursor.execute(''' DELETE FROM table_name WHERE condition ''')
 
#Saving the Actions performed on the DB
mysql.connection.commit()
 
#Closing the cursor
cursor.close()

login_manager = LoginManager()
login_manager.init_app(app)

from badger_bot import routes
    
