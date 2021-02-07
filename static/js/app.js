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

var socket = io.connect('http://localhost:5000');
//var socket = io.connect('https://activity-online.herokuapp.com/');

var explainTime = 15;
var drawTime = 30;
var pantomimeTime = 60;
let minTime = 5;

function joinRoom() {
    var roomName = window.location.pathname.substring(1);
    console.log("Joined room " + roomName);
    socket.emit('join', {room: roomName});
}

function showNewWord(guessTime) {
	document.getElementById("reset").innerHTML = "";
    var roomName = window.location.pathname.substring(1);
	socket.emit('getWord', {time: guessTime, room: roomName});
	console.log("asked for word with time "+guessTime+" in room "+roomName);
}

function handleReset() {
    var roomName = window.location.pathname.substring(1);
	socket.emit('reset', {room: roomName});
	console.log("asked for reset in room "+roomName);
}

function sendFinish() {
    var roomName = window.location.pathname.substring(1);
	socket.emit('finish', {room: roomName});
	console.log("asked to finish in room "+roomName);
}

function disableAllBtn() {	
  $(" #btn_explain ").prop('disabled', true);
  $(" #btn_explainPlus ").prop('disabled', true);
  $(" #btn_explainMinus ").prop('disabled', true);
  $(" #btn_draw ").prop('disabled', true);
  $(" #btn_drawPlus ").prop('disabled', true);
  $(" #btn_drawMinus ").prop('disabled', true);
  $(" #btn_pantomime ").prop('disabled', true);
  $(" #btn_pantomimePlus ").prop('disabled', true);
  $(" #btn_pantomimeMinus ").prop('disabled', true);
  $(" #btn_reset ").prop('disabled', true);
}

function enableAllBtn() {	
  $(" #btn_explain ").prop('disabled', false);
  $(" #btn_explainPlus ").prop('disabled', false);
  $(" #btn_explainMinus ").prop('disabled', false);
  $(" #btn_draw ").prop('disabled', false);
  $(" #btn_drawPlus ").prop('disabled', false);
  $(" #btn_drawMinus ").prop('disabled', false);
  $(" #btn_pantomime ").prop('disabled', false);
  $(" #btn_pantomimePlus ").prop('disabled', false);
  $(" #btn_pantomimeMinus ").prop('disabled', false);
  $(" #btn_reset ").prop('disabled', false);  
}

socket.on('guess', function(time) {
	console.log("Received guess time: " + time);
	if (isStopped()) {
		newLimit(time);
		startTimer();
		disableAllBtn();
		document.getElementById("word").innerHTML = "Guess!";
	}
});

socket.on('word', function(word, time) {
	if (isStopped()) {
		console.log("Received word: " + word );
		console.log("Received time: " + time );
		newLimit(time);
		startTimer();
		disableAllBtn();
		document.getElementById("word").innerHTML = "Your word is: " + word;
		document.getElementById("btn_finish").style.display='initial';
	}
});

socket.on('finish', function() {
	console.log("Received finish");
	stopResetTimer();
});

socket.on('resetPerformed', function() {
	console.log("Received reset performend");
	document.getElementById("reset").innerHTML = "Wordlist reloaded."
	enableAllBtn();
});

socket.on('resetRequired', function() {
	console.log("Received reset required");
	document.getElementById("word").innerHTML = "No more words, please reload word list."
	disableAllBtn();
	$(" #btn_reset ").prop('disabled', false);
});

$(" #btn_explainPlus ").click(function() {
	explainTime+=5;
	document.getElementById("btn_explain").innerHTML = "Explain ("+explainTime+" sec)";
});
$(" #btn_explainMinus ").click(function() {
	if (explainTime > minTime) {
		explainTime-=5;
		document.getElementById("btn_explain").innerHTML = "Explain ("+explainTime+" sec)";
	}
});
$(" #btn_drawPlus ").click(function() {
	drawTime+=5;
	document.getElementById("btn_draw").innerHTML = "Draw ("+drawTime+" sec)";
});
$(" #btn_drawMinus ").click(function() {
	if (drawTime > minTime) {
		drawTime-=5;
		document.getElementById("btn_draw").innerHTML = "Draw ("+drawTime+" sec)";
	}
});
$(" #btn_pantomimePlus ").click(function() {
	pantomimeTime+=5;
	document.getElementById("btn_pantomime").innerHTML = "Pantomime ("+pantomimeTime+" sec)";
});
$(" #btn_pantomimeMinus ").click(function() {
	if (pantomimeTime > minTime) {
		pantomimeTime-=5;
		document.getElementById("btn_pantomime").innerHTML = "Pantomime ("+pantomimeTime+" sec)";
	}
});

$(" #btn_explain ").click(function() {showNewWord(explainTime);});
$(" #btn_draw ").click(function() {showNewWord(drawTime);});
$(" #btn_pantomime ").click(function() {showNewWord(pantomimeTime);});
$(" #btn_reset ").click(function() {handleReset();});
$(" #btn_finish ").click(function() {sendFinish();});

window.onload = joinRoom;
