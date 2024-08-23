from flask import json, make_response, jsonify
import env, hashlib, time
from azure.storage.blob import BlobServiceClient

import mysql.connector
import app
class playlist_model():
    
    def create_playlist(self, f):
        data = f.form
        name = data['name']
        description = data['description']
        userid = data['userid']
        image = f.files.get('thumb')
        hash_guid_object = hashlib.sha256(name.encode())
        guid = hash_guid_object.hexdigest()
        img_url = ''
        ##
        ##take record file and upload to blob 
        conn = app.get_db_connection()
        if conn is None:
            return make_response(jsonify({"error": "Unable to connect to database"}), 500)
        if image:
            i_name = data['description'] + 'img'
            blob_service_client = BlobServiceClient.from_connection_string(env.BLOB.get('connection_string'))
            blob_client = blob_service_client.get_blob_client(container=env.BLOB.get('container_name'), blob = i_name)
            blob_client.upload_blob(image.stream)
            img_url = blob_client.url
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(f"""
                INSERT INTO `userplaylist`(`guid`,`playlistname`,`userid`, `description`, `thumb`) VALUES('{guid}','{name}', 
              '{userid}', '{description}', '{img_url}') """)
            conn.commit()
            return make_response('add success', 200)
        except Exception as e:
                print(f"An error occurred: {e}")
                return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()

    def get_playlist(self, id):
        try:
            conn = app.get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(f""" select * from userplaylist where userid = '{id}' """)
            result = cur.fetchall()
            if(len(result) > 0):
                return make_response(json.dumps(result), 200)
            else: return  make_response('No data found', 400)
        except Exception as e:
                print(f"An error occurred: {e}")
                return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()
        

    def get_systemPlaylist(self, id):
        try:
            conn = app.get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(f""" select * from systemplaylist where guid = '{id}' """)
            result = cur.fetchall()
            if(len(result) > 0):
                return make_response(json.dumps(result), 200)
            else: return  make_response('No data found', 400)
        except Exception as e:
                print(f"An error occurred: {e}")
                return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()
        