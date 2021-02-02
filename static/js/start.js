//var socket = io.connect('http://localhost:5000');
var socket = io.connect('https://activity-online.herokuapp.com/');

function createRoom() {
    var roomName = $(" #roomName ").val();
    console.log("Created room " + roomName);    
    window.open("https://activity-online.herokuapp.com/"+roomName,"_self")
}

$(" #btn_room ").click(function() {createRoom();});
