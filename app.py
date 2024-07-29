from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def welcome():
    return 'MeloSpace API'
<<<<<<< HEAD
# import controllers.song_controller
=======
import controllers.song_controller
>>>>>>> 8042adac7783d6ffb0a966516ddb9c4329a0c4e2
