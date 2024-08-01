from flask import json, make_response
from azure.storage.blob import BlobServiceClient
import env, hashlib, time
import mysql.connector
class record_model:
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host = 'localhost', user = 'root', password='12345678', database='melospacedb')
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('ok')
        except:
            print('fault')
    def get_record(self, id, cate, album):
        conditions = []
        if id:
            conditions.append(f"guid = '{id}'")
        if cate:
            conditions.append(f"cateID =  {cate} ")
        if album:
            conditions.append(f"albumID = '{album}'")

        where_clause = ' and '.join(conditions)
    
        if not where_clause:
            where_clause = '1=1'
        
        try:
            self.cur.execute(f"select * from record where {where_clause} ")
        except:
            return make_response('fail')
        result = self.cur.fetchall()
        if(len(result) > 0):
            return make_response(json.dumps(result), 200)
        else: return  make_response('No data found', 400)

    def add_new_record(self, data):
        form = data.form
        file = data.files.get('file')

        ##take record file and upload to blob

        blob_service_client = BlobServiceClient.from_connection_string(env.BLOB.get('connection_string'))
        blob_client = blob_service_client.get_blob_client(container=env.BLOB.get('container_name'), blob= form['recordname'])
        blob_client.upload_blob(file.stream)
        url =  blob_client.url
        ## create guid 
        current_time = str(time.time())
        name = form['recordname']
        combined_string = name + current_time
        hash__guid_object = hashlib.sha256(combined_string.encode())
        guid = hash__guid_object.hexdigest()

        ## insert
        try:
            self.cur.execute(f"""INSERT INTO `record`(`RecordName`,`RecordThumb`,`RecordURL`,`Duration`,`AuthID`,`Lyrics`,`View`,`AlbumID`,`LikeQuantity`,`ModeID`,`CateID`,`guid`) 
                    VALUES('{form['recordname']}','{form['recordthumb']}','{url}',{form['duration']},{form['authid']},'{form['lyrics']}',0,
                    {form['albumid']},0,{form['modeid']},{form['cateid']},'{guid}')""")
            return make_response('add susscess', 200)
        except:
            return make_response('fail')
        
    def add_to_album(self, data ):
        try:
            self.cur.execute(f"""
                UPDATE record
                SET albumid = '{data['albumid']}'
                WHERE guid = '{data['recordid']}'; """)
            return make_response('update sussess', 200)
        except:
            return make_response('Cannot update', 400)