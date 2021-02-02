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
socketio = SocketIO(app, cors_allowed_origins='*', ping_interval = (25, 25), ping_timeout = 15)#, logger=True, engineio_logger=True)

#TODO get word list from client
ds = {}

@app.route("/")
def welcome():
    return render_template('index.html', room_name_suggest=generate_slug(2))
    
@app.route('/<string:roomName>')
def enter_room(roomName):
    #TODO Add sessions for users to start in individual rooms!
    ds[roomName] = DataStore()
    return render_template('room.html', room_name=roomName)
        
@socketio.on('connect')
def connect():
    print('Client connected: '+str(request.sid))
    
@socketio.on('join')
def on_join(data):
    roomName = data['room']
    join_room(roomName)
    print('Client '+str(request.sid)+' joined the room', roomName)

@socketio.on('leave')
def on_leave(data):
    roomName = data['room']
    leave_room(roomName)
    print('Client '+str(request.sid)+' left the room', roomName)

@socketio.on('getWord')
def getWord(data):
    time = data["time"]
    room = data.pop('room')
    print('received getWord with time: ' + str(time) + ' in room '+room)
    if ds[room].isEmpty():
        emit('resetRequired', room=room)
    else:
        word = ds[room].getRandomElement()
        emit('guess', time, room=room, include_self=False) #broadcast=True
        emit('word', (word, time), room=request.sid, namespace='')

@socketio.on('reset')
def reset(data):
    roomName = data['room']
    ds[roomName].reset()
    emit('resetPerformed', room=roomName)

@socketio.on('disconnect')
def disconnect():
    #if room empty clean up ds[roomName]
    print('Client disconnected: '+str(request.sid))

#Not called by heroku
if __name__ == '__main__':
    socketio.run(app)

    
