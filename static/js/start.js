//Activity Online - an online guessing game
//Copyright (C) 2021 Peter Munk

//This program is free software: you can redistribute it and/or modify
//it under the terms of the GNU Affero General Public License as
//published by the Free Software Foundation, either version 3 of the
//License, or (at your option) any later version.

//This program is distributed in the hope that it will be useful,
//but WITHOUT ANY WARRANTY; without even the implied warranty of
//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//GNU Affero General Public License for more details.

//You should have received a copy of the GNU Affero General Public License
//along with this program.  If not, see <https://www.gnu.org/licenses/>.

//var socket = io.connect('http://localhost:5000');
var socket = io.connect('https://activity-online.herokuapp.com/');

function createRoom() {
    var roomName = $(" #roomName ").val();
    console.log("Created room " + roomName);    
    //window.open("http://localhost:5000/"+roomName,"_self")
    window.open("https://activity-online.herokuapp.com/"+roomName,"_self")
}

$(" #btn_room ").click(function() {createRoom();});
