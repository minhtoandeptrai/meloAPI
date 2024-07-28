from models.song_model import song_model
from flask import request
from app import app
#base url: http://127.0.0.1:5000
song = song_model()

@app.route('/song/getAll')
def user_get():
    return song.get_all_song()
