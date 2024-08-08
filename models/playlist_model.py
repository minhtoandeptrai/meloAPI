from flask import json, make_response
import env, hashlib, time
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
    
    def create_playlist(self, data):
        name = data['playlistname']
        print(name)
        hash_guid_object = hashlib.sha256(name.encode())
        guid = hash_guid_object.hexdigest()
        try:
            self.cur.execute(f"""
                INSERT INTO `userplaylist`(`guid`,`playlistname`,`userid`) VALUES('{guid}','{name}',
               '{data['userid']}') """)
            return make_response('add success', 200)
        except:
            return make_response("fail")
    
    def get_playlist(self, id):
        try:
            self.cur.execute(f""" select * from userplaylist where userid = '{id}' """)
        except:
            return make_response("fail")
        result = self.cur.fetchall()
        if(len(result) > 0):
            return make_response(json.dumps(result), 200)
        else: return  make_response('No data found', 400)
