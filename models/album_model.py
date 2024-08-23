from flask import json, make_response, jsonify
from azure.storage.blob import BlobServiceClient
import env, hashlib, time
import mysql.connector
import app
class album_model:
    def get_album(self, id, alID):
        conn = app.get_db_connection()
        if conn is None:
            return make_response(jsonify({"error": "Unable to connect to database"}), 500)
        if id:
            try:
                cur = conn.cursor(dictionary=True)
                cur.execute(f"""select * from album where userid = '{id}'""")
            except:
                return make_response("fail", 400)
            result =  cur.fetchall()
            if(len(result) > 0):
                return make_response(json.dumps(result), 200)
            else: return  make_response('No data found', 400)
        elif alID:
            try:
                cur = conn.cursor(dictionary=True)
                cur.execute(f"""select * from album where guid = '{alID}'""")
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
            
    def create_album(self, f):
        data = f.form
        name = data['albumname']
        image = f.files.get('thumb')

        hash_guid_object = hashlib.sha256(name.encode())
        guid = hash_guid_object.hexdigest()

        img_url = ''
        if image:
            i_name = data['description'] + 'img'
            blob_service_client = BlobServiceClient.from_connection_string(env.BLOB.get('connection_string'))
            blob_client = blob_service_client.get_blob_client(container=env.BLOB.get('container_name'), blob = i_name)
            blob_client.upload_blob(image.stream)
            img_url = blob_client.url
        try:
            conn = app.get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(f"""
                INSERT INTO `album`(`guid`,`albumname`,`albumthumb`,`userid`, `description`) VALUES('{guid}','{name}',
                '{img_url}','{data['userid']}', '{data['description']}') """)
            conn.commit()
            
            return make_response('add success', 200)
        except Exception as e:
                print(f"An error occurred: {e}")
                return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()
    
    def update_album(self,data):
        id = data['albumid']
        isUpdate = False
        if 'albumname' in data:
            self.cur.execute(f"""
                UPDATE album
                SET albumname = '{data['albumname']}'
                WHERE guid = '{id}';
            """)
            isUpdate = True

        if 'albumthumb' in data:
            self.cur.execute(f"""
                UPDATE album
                SET albumthumb = '{data['albumthumb']}'
                WHERE guid = '{id}';
            """)
            isUpdate = True
        
        if isUpdate == True:
            return make_response('update susscess', 200)
        else: return make_response('Unexpected')