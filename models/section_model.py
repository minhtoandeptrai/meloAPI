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

    def get_DanhChoBan(self):
        try:
            self.cur.execute(f"""
                        SELECT * 
                            from section inner join sectionplaylist 
                            on section.id = sectionplaylist.id_section
                            inner join systemplaylist
                            on sectionplaylist.id_playlist = systemplaylist.playlistid
                            where section.id = 1""")
        except:
            return 'Fail'
        result = self.cur.fetchall()
        if(len(result) > 0):
            return make_response(json.dumps(result), 200)
        else: return  make_response('No data found', 400)
    def get_AlbumNoiBat(self):
        try:
            self.cur.execute(f"""
                        SELECT * 
                            from section inner join sectionplaylist 
                            on section.id = sectionplaylist.id_section
                            inner join systemplaylist
                            on sectionplaylist.id_playlist = systemplaylist.playlistid
                            where section.id = 2""")
        except:
            return 'Fail'
        result = self.cur.fetchall()
        if(len(result) > 0):
            return make_response(json.dumps(result), 200)
        else: return  make_response('No data found', 400)        
    def get_NguoiDungNoiBat(self):
        try:
            self.cur.execute(f"""
                        SELECT * 
                            from section inner join sectionplaylist 
                            on section.id = sectionplaylist.id_section
                            inner join systemplaylist
                            on sectionplaylist.id_playlist = systemplaylist.playlistid
                            where section.id = 3""")
        except:
            return 'Fail'
        result = self.cur.fetchall()
        if(len(result) > 0):
            return make_response(json.dumps(result), 200)
        else: return  make_response('No data found', 400)
    def get_DanhSanhPhatNoiBat(self):
        try:
            self.cur.execute(f"""
                        SELECT * 
                            from section inner join sectionplaylist 
                            on section.id = sectionplaylist.id_section
                            inner join systemplaylist
                            on sectionplaylist.id_playlist = systemplaylist.playlistid
                            where section.id = 3""")
        except:
            return 'Fail'
        result = self.cur.fetchall()
        if(len(result) > 0):
            return make_response(json.dumps(result), 200)
        else: return  make_response('No data found', 400)