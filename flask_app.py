# inspired by https://towardsdatascience.com/build-a-simple-web-app-with-github-pages-flask-and-heroku-bcb2dacc8331
#and https://medium.com/the-andela-way/deploying-a-python-flask-app-to-heroku-41250bda27d0

#(c) Peter Munk 2020

import os
from coolname import generate_slug
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
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
    return render_template('index.html', room_name_suggest=generate_slug())
#    return (f"Activity API<br>")
    
@app.route('/path/<string:roomName>')
def enter_room(roomName):
    # show the subpath after /path/
    return 'Subpath %s' % escape(roomName)
        
@socketio.on('connect')
def connect():
    print('Client connected: '+str(request.sid))
    
@socketio.on('join')
def on_join(data):
    roomName = data['room']
    join_room(roomName)
    print('Entered the room', roomName)

@socketio.on('leave')
def on_leave(data):
    roomName = data['room']
    leave_room(roomName)
    print('left the room.', roomName)
        
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

#Not called by heroku
if __name__ == '__main__':
    socketio.run(app)
