from flask import Flask
from mysql.connector import errorcode
from flask_cors import CORS
import mysql.connector
from mysql.connector import pooling

dbconfig = {
    "user": "root",
    "password": "123123",
    "host": "localhost",
    "database": "melospace"
}
app = Flask(__name__)
CORS(app)

cnxpool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)
def get_db_connection():
    try:
        return cnxpool.get_connection()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    

@app.route('/')
def welcome():

    return 'MeloSpace API'

import controllers.user_controller
import controllers.record_controller
import controllers.album_controller
import controllers.playlist_controller
import controllers.login_google_controller
import controllers.section_controller