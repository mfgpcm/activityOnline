# -*- coding: utf-8 -*-
#Activity Online - an online guessing game
#Copyright (C) 2021 Peter Munk

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as
#published by the Free Software Foundation, either version 3 of the
#License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.

#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

#not in main for heroku 
ds = {}
availableFiles = DataStore.getAvailableLists()

@app.route("/")
def welcome():
    return render_template('index.html', room_name_suggest=generate_slug(2), files=availableFiles)
    
@app.route('/<string:roomName>', methods=['GET', 'POST'])
def enter_room(roomName):
    # TODO return a favicon.ico
    # handle the POST request
    if request.method == 'POST':
        if roomName in ds:
            print("Room "+roomName+" already exists, resetting data store.")
        wordListSet = request.form.getlist('wordListSet')
        print('Client created the room', roomName)
        print('selected word lists: '+format(wordListSet))
        ds[roomName] = DataStore()
        if "ownWords" in wordListSet:
            wordListSet.remove("ownWords")
            ownWords = request.form['ownWordList']
            if ownWords:
                ds[roomName].parseCustomWordList(ownWords)
                DataStore.saveCustomWordList(ownWords, roomName)
        ds[roomName].loadWordSets(wordListSet)
    # handle the GET request
    if not(roomName in ds):
        print("Room "+roomName+" was not initialized, loading default word list Easy 1.")
        #room was not created, so we load default word list
        ds[roomName] = DataStore()
        ds[roomName].loadWordSets(['Easy 1'])
    return render_template('room.html', room_name=roomName, wordSets=ds[roomName].getWordLists(), ownWords=ds[roomName].usesOwnWord())
        
@socketio.on('connect')
def connect():
    print('Client connected: '+str(request.sid))
    
@socketio.on('join')
def on_join(data):
    roomName = data['room']
    join_room(roomName)
    print('Client '+str(request.sid)+' joined the room '+ roomName)

@socketio.on('leave')
def on_leave(data):
    roomName = data['room']
    leave_room(roomName)
    print('Client '+str(request.sid)+' left the room '+ roomName)

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
        emit('word', (word, time), room=request.sid)

@socketio.on('finish')
def finish(data):
    roomName = data['room']
    emit('finish', room=roomName)

@socketio.on('reset')
def reset(data):
    roomName = data['room']
    ds[roomName].reset()
    emit('resetPerformed', room=roomName)

@socketio.on('disconnect')
def disconnect():
    #TODO if room empty clean up ds[roomName]
    print('Client disconnected: '+str(request.sid))

#Not called by heroku
if __name__ == '__main__':
    socketio.run(app)

    
