// script.js
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
