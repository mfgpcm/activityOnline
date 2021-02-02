//var socket = io.connect('http://localhost:5000');
var socket = io.connect('https://activity-online.herokuapp.com/');

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

function disableAllBtn() {	
  $(" #btn_explain ").prop('disabled', true);
  $(" #btn_draw ").prop('disabled', true);
  $(" #btn_pantomime ").prop('disabled', true);
}

function enableAllBtn() {	
  $(" #btn_explain ").prop('disabled', false);
  $(" #btn_draw ").prop('disabled', false);
  $(" #btn_pantomime ").prop('disabled', false);
}


socket.on('guess', function(time) {
	console.log("Received guess time:" + time);
	newLimit(time);
	startTimer();
	disableAllBtn();
	document.getElementById("word").innerHTML = "Guess!";
});

socket.on('word', function(word, time) {
	console.log("Received word: " + word );
	console.log("Received time: " + time );
	newLimit(time);
	startTimer();
	disableAllBtn();
	document.getElementById("word").innerHTML = "Your word is: " + word;
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
});

$(" #btn_explain ").click(function() {showNewWord(15);});
$(" #btn_draw ").click(function() {showNewWord(30);});
$(" #btn_pantomime ").click(function() {showNewWord(60);});
$(" #btn_reset ").click(function() {handleReset();});

window.onload = joinRoom;
