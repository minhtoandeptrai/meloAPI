from flask import Flask
app = Flask(__name__)
@app.route('/')
def welcome():
    return 'MeloSpace API'
import controllers.song_controller
