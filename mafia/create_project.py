import os

def create_project_structure():
    # Define the project directory and subdirectories
    project_name = 'mafia-game'
    directories = [
        f"{project_name}/templates",
        f"{project_name}/static",
        f"{project_name}/static/css",
        f"{project_name}/static/js"
    ]

    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

    # Create the main app.py file (backend)
    app_code = '''from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

# List to store the players and their roles
players = []
roles = []
game_started = False

# Game roles
all_roles = ['Mafia', 'Mafia', 'Mafia', 'Villager', 'Villager', 'Detective', 'Doctor', 'Villager', 'Villager', 'Villager', 'Killer']

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join_game')
def handle_join_game(username):
    global players
    players.append({'username': username, 'id': request.sid})
    emit('player_list', [player['username'] for player in players], broadcast=True)

@socketio.on('start_game')
def handle_start_game():
    global roles, game_started
    if len(players) >= 6:
        random.shuffle(all_roles)
        roles = {player['id']: all_roles[i] for i, player in enumerate(players)}
        game_started = True
        emit('game_started', roles, broadcast=True)
    else:
        emit('error_message', "Not enough players to start the game.")

@socketio.on('player_action')
def handle_player_action(action_data):
    # Process player actions such as voting or investigating
    print(f"Player action received: {action_data}")
    emit('game_update', action_data, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    global players
    players = [player for player in players if player['id'] != request.sid]
    emit('player_list', [player['username'] for player in players], broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
'''

    with open(f'{project_name}/app.py', 'w') as f:
        f.write(app_code)
        print("Created app.py (backend)")

    # Create the HTML file (frontend)
    html_code = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mafia Game</title>
  <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
  <div id="game-container">
    <h1>Mafia Game</h1>
    
    <div id="player-list">
      <!-- Player list will appear here -->
    </div>

    <div id="game-actions">
      <!-- Game actions (e.g., Vote, Investigate, Protect) -->
    </div>

    <div id="chat-box">
      <!-- Chat window -->
    </div>
    
    <button id="start-game-btn">Start Game</button>
  </div>

  <script src="https://cdn.socket.io/4.4.1/socket.io.min.js"></script>
  <script src="static/js/script.js"></script>
</body>
</html>
'''

    with open(f'{project_name}/templates/index.html', 'w') as f:
        f.write(html_code)
        print("Created index.html (frontend)")

    # Create the CSS file
    css_code = '''/* style.css */
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f9;
  text-align: center;
}

#game-container {
  margin-top: 50px;
}

#player-list {
  margin: 20px;
}

#game-actions {
  margin-top: 20px;
}

#chat-box {
  margin-top: 20px;
  height: 200px;
  overflow-y: scroll;
  border: 1px solid #ccc;
  padding: 10px;
  background-color: #fff;
}
'''

    with open(f'{project_name}/static/css/style.css', 'w') as f:
        f.write(css_code)
        print("Created style.css (styling)")

    # Create the JavaScript file
    js_code = '''// script.js
// Connect to the server via Socket.IO
const socket = io();

// Function to handle game start
document.getElementById('start-game-btn').addEventListener('click', () => {
  const username = prompt("Enter your username:");
  socket.emit('join_game', username); // Send username to the server
});

// Update player list on the frontend
socket.on('player_list', (players) => {
  const playerListDiv = document.getElementById('player-list');
  playerListDiv.innerHTML = 'Players: ' + players.join(', ');
});

// Notify when the game starts and assign roles
socket.on('game_started', (roles) => {
  console.log("Game started! Roles:", roles);
  alert("Game started! Your role is: " + roles[Object.keys(roles).find(key => roles[key] === roles[key])]);
});

// Error handling if there are not enough players to start
socket.on('error_message', (message) => {
  alert(message);
});
'''

    with open(f'{project_name}/static/js/script.js', 'w') as f:
        f.write(js_code)
        print("Created script.js (frontend logic)")

    # Create requirements.txt for Python dependencies
    requirements_code = '''Flask
Flask-SocketIO
'''

    with open(f'{project_name}/requirements.txt', 'w') as f:
        f.write(requirements_code)
        print("Created requirements.txt for dependencies")

    print(f"Project '{project_name}' created successfully!")

if __name__ == "__main__":
    create_project_structure()
