# inspired by https://towardsdatascience.com/build-a-simple-web-app-with-github-pages-flask-and-heroku-bcb2dacc8331

from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dataStore import DataStore

app = Flask(__name__)
#app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'adfpoihq34trihu34g9uph'
cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*') #, logger=True, engineio_logger=True)

#TODO get word list from client
#Add sessions for users to start in individual rooms!
ds = DataStore()

@app.route("/")
def welcome():
    return (f"Activity API<br>")
        
@socketio.on('connect')
def connect():
    print('Client connected: '+str(request.sid))
        
@socketio.on('getWord')
def getWord(data):
    time = data["time"]
    print('received time: ' + str(time))
    if ds.isEmpty():
        emit('resetRequired', broadcast=True)
    else:
        word = ds.getRandomElement()        
        emit('word', (word, time), broadcast=False)
        emit('guess', time, broadcast=True, include_self=False)

@socketio.on('reset')
def reset():
    ds.reset()
    emit('resetPerformed', broadcast=True)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected: '+str(request.sid))

#Not called by pythonanywhere!     
if __name__ == '__main__':
    #ds = DataStore()
    #app.run()
    socketio.run(app)
    