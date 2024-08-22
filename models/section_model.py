from flask import json, make_response, jsonify
from azure.storage.blob import BlobServiceClient
import app
class section_model:
    def get_all_section(self):
        conn = app.get_db_connection()
        if conn is None:
            return make_response(jsonify({"error": "Unable to connect to database"}), 500)
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(f"""
                SELECT * from section """)
            result = cur.fetchall()
            if(len(result) > 0):
                return make_response(json.dumps(result), 200)
            else: return  make_response('No data found', 200)
        except:
            return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()
    def get_section_item(self, id):
        conn = app.get_db_connection()
        if conn is None:
            return make_response(jsonify({"error": "Unable to connect to database"}), 500)
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(f"""
                SELECT * FROM melospace.sectionitem
                where sectionid = {id} """)
            result = cur.fetchall()
            if(len(result) > 0):
                return make_response(json.dumps(result), 200)
            else: return  make_response('No data found', 200)
        except Exception as e:
            print(f"An error occurred: {e}")
            return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()
    

        