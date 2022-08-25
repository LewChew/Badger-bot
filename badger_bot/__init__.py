import sqlite3
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import pprint
import json
import urllib3
import os

load_dotenv()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://"+ os.environ.get('MYSQL_USER','sqlite') + ":" + os.environ.get('MYSQL_PASSWORD',)+ "@" + os.environ.get('MYSQL_HOST',) + ":3306/badger"


app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

mysql = SQLAlchemy(app) 

#Executing SQL Statements

from .models import mysql
mysql.create_all()
mysql.session.commit()

from .routes import *
    
