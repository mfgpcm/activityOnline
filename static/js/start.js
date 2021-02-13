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

function createRoom() {
    var roomName = $(" #roomName ").val();
    console.log("Created room " + roomName);    
	$(" #form ").attr({'action': '/'+roomName});
	$(" #btn_room ").attr({'type': 'submit'});
	$(" #btn_room ").submit();
}

$(" #btn_room ").click(function() {createRoom();});

$(" #btn_room ").click(function() {createRoom();});

$('#cb_own').click(function(){
    if($(this).is(':checked')){
		document.getElementById("textOwnWords").style.display='flex';
    } else {
		document.getElementById("textOwnWords").style.display='none';
	}
});

function validateRoomName() {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
}

window.onload = validateRoomName;

