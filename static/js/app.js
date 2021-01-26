var socket = io.connect('http://localhost:5000');
//var socket = io.connect('https://mfgpcm.pythonanywhere.com');
//var socket = io.connect('https://activity-backend.herokuapp.com/');

function createRoom(guessTime) {
    var roomName = $(" #roomName ").val();
  	console.log("Created room " + roomName);
	socket.emit('join', {room: roomName});
}
	
function showNewWord(guessTime) {
	document.getElementById("reset").innerHTML = "";	
	socket.emit('getWord', {time: guessTime});
	console.log("asked for word with time "+guessTime);
}

function handleReset() {
	socket.emit('reset');
	console.log("asked for reset");
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

$(" #btn_room ").click(function() {createRoom();});
$(" #btn_explain ").click(function() {showNewWord(15);});
$(" #btn_draw ").click(function() {showNewWord(30);});
$(" #btn_pantomime ").click(function() {showNewWord(60);});
$(" #btn_reset ").click(function() {handleReset();});
