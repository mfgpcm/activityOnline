# Activity Online

This is a WebApp using pyhton flask socketio API that is supposed to run at https://activity-backend.herokuapp.com.
Initially it reads a CSV file with words and serves each requesting client a word, removing it from the list and sending a guess time to all other clients.
The word list can be reloaded on request.

## TODOs:
* Change the default word list to a more common one
* Allow users to upload own word lists.
