from flask import Flask
from mysql.connector import errorcode
from flask_cors import CORS
import mysql.connector
app = Flask(__name__)
CORS(app)

@app.route('/')
def welcome():
   
    return 'MeloSpace API'

import controllers.user_controller
import controllers.record_controller
import controllers.album_controller
import controllers.playlist_controller
import controllers.login_google_controller
