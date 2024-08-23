from flask import json, make_response
from azure.storage.blob import BlobServiceClient
import env, hashlib, time
import mysql.connector
from mysql.connector import errorcode
import app
class record_model:
    def get_record(self, user, id, cate, album):
        conditions = []
        if id:
            conditions.append(f"guid = '{id}'")
        if cate:
            conditions.append(f"cateID =  {cate} ")
        if album:
            conditions.append(f"albumID = '{album}'")
        if user:
            conditions.append(f"authID = '{user}'")
        where_clause = ' and '.join(conditions)
    
        if not where_clause:
            where_clause = '1=1'
        
        try:
            conn = app.get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(f"select * from record where {where_clause} and deleted = 0")
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
        
        
    def add_new_record(self, data):
        form = data.form
        file = data.files.get('record')
        image = data.files.get('image')
        ##take record file and upload to blob 
        blob_service_client = BlobServiceClient.from_connection_string(env.BLOB.get('connection_string'))
        blob_client = blob_service_client.get_blob_client(container=env.BLOB.get('container_name'), blob= form['recordname'])
        blob_client.upload_blob(file.stream)
        record_url =  blob_client.url

        ##upload img
        name = form['recordname'] + 'img'
        blob_service_client = BlobServiceClient.from_connection_string(env.BLOB.get('connection_string'))
        blob_client = blob_service_client.get_blob_client(container=env.BLOB.get('container_name'), blob = name)
        blob_client.upload_blob(image.stream)
        img_url =  blob_client.url

        ## create guid 
        current_time = str(time.time())
        name = form['recordname']
        combined_string = name + current_time
        hash__guid_object = hashlib.sha256(combined_string.encode())
        guid = hash__guid_object.hexdigest()

        ## insert
        try:
            conn = app.get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(f"""INSERT INTO `record`(`RecordName`,`RecordURL`,`RecordThumb`,`AuthID`,
                `ModeID`,`guid`,`deleted`,`CateID`,`AlbumID`) VALUES('{form['recordname']}','{record_url}','{img_url}','{form['authid']}',
                    {form['modeid']},'{guid}',0,'{form['cateid']}','{form['albumid']}');""")
            return make_response('add susscess', 200)
        except Exception as e:
                print(f"An error occurred: {e}")
                return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()
        
    def add_to_album(self, data ):
        try:
            conn = app.get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(f"""
                UPDATE record
                SET albumid = '{data['albumid']}'
                WHERE guid = '{data['recordid']}'; """)
            return make_response('update sussess', 200)
        except Exception as e:
                print(f"An error occurred: {e}")
                return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()
        
    def hide_record(self, data):
        try:
            conn = app.get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(f"""
                UPDATE record 
                set deleted = 1
                where guid = '{data['id']}'; """)
            return make_response('sussess', 200)
        except Exception as e:
                print(f"An error occurred: {e}")
                return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()