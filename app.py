from flask import Flask
<<<<<<< HEAD
import controllers.song_controller
=======
>>>>>>> b92e1a29865c34ebdba52bb22b3c4fcc29eb80eb

app = Flask(__name__)

@app.route('/')
def welcome():
<<<<<<< HEAD
    return 'MeloSpace API'
=======
    return 'MeloSpace API'

import controllers.song_controller
>>>>>>> b92e1a29865c34ebdba52bb22b3c4fcc29eb80eb
