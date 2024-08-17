from flask import json, make_response
from azure.storage.blob import BlobServiceClient
import env, hashlib, time
import mysql.connector
class section_model:
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host = 'localhost', user = 'root', password='123123', database='melospace')
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('ok')
        except:
            print('fault')

    def get_all_section(self):
        try:
            self.cur.execute(f"""
                        SELECT * from section """)
        except:
            return 'Fail'
        result = self.cur.fetchall()
        if(len(result) > 0):
            return make_response(json.dumps(result), 200)
        else: return  make_response('No data found', 400)
    def get_section_item(self, id):
        result = []
        if id == '1':
            try:
                self.cur.execute(f"""
                    SELECT * FROM melospace.sectionitem
                    inner join user 
                    on sectionitem.userid = user.guid; """)
            except:
                return 'Fail'
            result = self.cur.fetchall()
        elif id == '2':
            try:
                self.cur.execute(f"""
                    SELECT * FROM melospace.sectionitem
                        inner join album 
                        on sectionitem.albumid = album.guid; """)
            except:
                return 'Fail'
            result = self.cur.fetchall()
        elif id == '3':
            try:
                self.cur.execute(f"""
                    SELECT * FROM melospace.sectionitem
                    inner join systemplaylist 
                    on sectionitem.playlistid = systemplaylist.guid; """)
            except:
                return 'Fail'
            result = self.cur.fetchall()
        if(len(result) > 0):
            return make_response(json.dumps(result), 200)
        else: return  make_response('No data found', 400)