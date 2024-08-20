from models.playlist_model import playlist_model
from models.auth_model import auth_model
from flask import request
from app import app

#base url: http://127.0.0.1:5000
playlist = playlist_model()
@app.route('/playlist')
def get_playlist():
    id = request.args.get('userid')
    return playlist.get_playlist(id=id)

@app.route('/playlist', methods=['post'])
def create_playlist():
    return playlist.create_playlist(request.form)

@app.route('/systemPl')
def get_systemPlaylist():
    print('pl')
    id = request.args.get('id')
    return playlist.get_systemPlaylist(id)
