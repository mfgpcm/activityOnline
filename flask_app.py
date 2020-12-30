# inspired by https://towardsdatascience.com/build-a-simple-web-app-with-github-pages-flask-and-heroku-bcb2dacc8331

from flask import Flask
from flask_cors import CORS
from dataStore import DataStore

app = Flask(__name__)
CORS(app)

#TODO get word list from client
#Add sessions for users to start in individual rooms!

ds = DataStore

@app.route("/")
def welcome():
    return (print(f"Activity API<br>"))
    
@app.route("/getWord")
def word():
    try:
        return (ds.getRandomElement())
    except Exception as e:
        return (f"{e}")

@app.route("/reset")
def reset():
    try:
        ds.reset()
        return (f"Word list reloaded")
    except Exception as e:
        return (f"{e}")
        
if __name__ == '__main__':
    ds = DataStore()
    app.run()