import base64
from flask import Flask
from mysql.connector import errorcode
from flask_cors import CORS
import mysql.connector
from mysql.connector import pooling
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
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
def decrypt_data(encrypted_data):
    with open('private_key.pem', 'rb') as f:
        private_key = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_data = base64.b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data.decode('utf-8')

@app.route('/')
def welcome():
    return 'MeloSpace API'

import controllers.user_controller
import controllers.record_controller
import controllers.album_controller
import controllers.playlist_controller
import controllers.login_google_controller
import controllers.section_controller