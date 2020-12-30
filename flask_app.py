# inspired by https://towardsdatascience.com/build-a-simple-web-app-with-github-pages-flask-and-heroku-bcb2dacc8331
#and https://medium.com/the-andela-way/deploying-a-python-flask-app-to-heroku-41250bda27d0

#(c) Peter Munk 2020

import os
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dataStore import DataStore

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ
app.config['SECRET_KEY'] = 'adfpoihq34trihu34g9uph'
cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*', ping_interval = (25, 25), ping_timeout = 15, ) #, logger=True, engineio_logger=True)

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
     gevent.sleep(0.1)
    print('received time: ' + str(time))
    gevent.sleep(0.1)
    if ds.isEmpty():
        gevent.sleep(0.1)
        emit('resetRequired', broadcast=True)
    else:
        word = ds.getRandomElement()        
        gevent.sleep(0.1)
        emit('word', (word, time), broadcast=False)
        gevent.sleep(0.1)
        emit('guess', time, broadcast=True, include_self=False)

@socketio.on('reset')
def reset():
    ds.reset()
    gevent.sleep(0.1)
    emit('resetPerformed', broadcast=True)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected: '+str(request.sid))
    gevent.sleep(0.1)

#Not called by pythonanywhere!     
if __name__ == '__main__':
    #ds = DataStore()
    #app.run()
    socketio.run(app)
    