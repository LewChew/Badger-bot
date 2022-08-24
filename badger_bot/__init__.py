import sqlite3
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pprint
import json
import urllib3
import os


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql://"+ os.environ['MYSQL_USER'] + ":" + os.environ['MYSQL_PASSWORD']+ "@" + os.environ['MYSQL_HOST'] + ":3306/badger")

app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

mysql = SQLAlchemy(app) 

#Executing SQL Statements

from .models import mysql
mysql.create_all()
mysql.session.commit()

from .routes import *
    
