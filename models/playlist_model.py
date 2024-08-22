from flask import json, make_response
import env, hashlib, time
from azure.storage.blob import BlobServiceClient

import mysql.connector

class playlist_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host = "localhost", user = "root", password= "123123", database= "melospace")
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('okk')
        except:
            print('fault')
    
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
        if image:
            i_name = data['description'] + 'img'
            blob_service_client = BlobServiceClient.from_connection_string(env.BLOB.get('connection_string'))
            blob_client = blob_service_client.get_blob_client(container=env.BLOB.get('container_name'), blob = i_name)
            blob_client.upload_blob(image.stream)
            img_url = blob_client.url
        try:
            self.cur.execute(f"""
                INSERT INTO `userplaylist`(`guid`,`playlistname`,`userid`, `description`, `thumb`) VALUES('{guid}','{name}', 
              '{userid}', '{description}', '{img_url}') """)
            return make_response('add success', 200)
        except :
            return make_response('fail', 400)
    
    def get_playlist(self, id):
        try:
            self.cur.execute(f""" select * from userplaylist where userid = '{id}' """)
        except:
            return make_response("fail")
        result = self.cur.fetchall()
        if(len(result) > 0):
            return make_response(json.dumps(result), 200)
        else: return  make_response('No data found', 400)

    def get_systemPlaylist(self, id):
        try:
            self.cur.execute(f""" select * from systemplaylist where guid = '{id}' """)
        except:
            return make_response("fail")
        result = self.cur.fetchall()
        if(len(result) > 0):
            return make_response(json.dumps(result), 200)
        else: return  make_response('No data found', 400)