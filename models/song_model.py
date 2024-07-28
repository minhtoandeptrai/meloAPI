from flask import json, make_response
import mysql.connector
class song_model:
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host = 'my1stsqlserver.mysql.database.azure.com', user = 'toanpython', password='Abcde123', database='mp3store')
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('ok')
        except:
            print('fault')
    def get_all_song(self):
        self.cur.execute(f"select * from song")
        result = self.cur.fetchall()
        if(len(result) > 0):
            return json.dumps(result)
        else: return  'No data found'