from flask import json, make_response
from azure.storage.blob import BlobServiceClient
import env, hashlib, time
import mysql.connector
class album_model:
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host = 'localhost', user = 'root', password='123123', database='melospace')
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('ok')
        except:
            print('fault')

    def get_album(self, id, alID):
        if id:
            try:
                self.cur.execute(f"""select * from album where userid = '{id}'""")
            except:
                return make_response("fail", 400)
            result = self.cur.fetchall()
            if(len(result) > 0):
                return make_response(json.dumps(result), 200)
            else: return  make_response('No data found', 400)
        elif alID:
            try:
                self.cur.execute(f"""select * from album where guid = '{alID}'""")
            except:
                return make_response("fail", 400)
            result = self.cur.fetchall()
            if(len(result) > 0):
                return make_response(json.dumps(result), 200)
            else: return  make_response('No data found', 400)
        
    def create_album(self, data):
        name = data['albumname']
        hash_guid_object = hashlib.sha256(name.encode())
        guid = hash_guid_object.hexdigest()
        try:
            self.cur.execute(f"""
                INSERT INTO `album`(`guid`,`albumname`,`albumthumb`,`userid`) VALUES('{guid}','{name}',
                '{data['albumthumb']}','{data['userid']}') """)
            return make_response('add success', 200)
        except:
            return make_response("fail")
    
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