# inspired by https://towardsdatascience.com/build-a-simple-web-app-with-github-pages-flask-and-heroku-bcb2dacc8331

from flask import Flask
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

ds = DataStore

@app.route("/")
def welcome():
    return (f"Activity API<br>")
        
@socketio.on('connect', namespace='/messages')
def connect():
    print('Client connected')
        
@socketio.on('getWord', namespace='/messages')
def getWord(data):
    time = data["time"]
    print('received time: ' + str(time))
    if ds.isEmpty():
        socketio.emit('resetRequired', namespace='/messages', broadcast=True)
    else:
        word = ds.getRandomElement()        
        socketio.emit('guess', time, namespace='/messages', broadcast=True)
        socketio.emit('word', word, namespace='/messages')

@socketio.on('reset', namespace='/messages')
def reset():
    ds.reset()
    socketio.emit('resetPerformed', namespace='/messages', broadcast=True)

@socketio.on('disconnect', namespace='/messages')
def disconnect():
    print('Client disconnected')
       
if __name__ == '__main__':
    ds = DataStore()
    #app.run()
    socketio.run(app)
    