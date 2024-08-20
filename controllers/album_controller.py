from models.album_model import album_model
from models.auth_model import auth_model
from flask import request
from app import app

#base url: http://127.0.0.1:5000
album = album_model()


@app.route('/album')
def get_album():
    id = request.args.get('userid')
    albumId = request.args.get('albumid')
    return album.get_album(id=id, alID=albumId)

@app.route('/album', methods=['post'])
def create_album():
    return album.create_album(request.form)

@app.route('/album/update', methods=['patch'])
def update_album():
    return album.update_album(request.form)