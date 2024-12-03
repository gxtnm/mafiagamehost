from flask import Flask, request, render_template, jsonify, session
import random
import sqlite3


app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session management

# Function to generate mafia mask (head part)
def print_mafia_mask(x):
    output = [
        "    -----   ",
        "   /     \\  ",
        "  /       \\ ",
        f" | player{x} |",
        "  \\       / ",
        "   \\_____/  "
    ]
    for _ in range(5):
        output.append("     |     ")
    output.append("     |     ")
    return "\n".join(output)

# Function to generate open mask with the role
def print_open_mask(x, role):
    racket = [
        "                 -----      ",
        "                /     \\     ",
        "               /       \\    ",
        "--------------|         |    ",
        "               \\       /     ",
        "                \\_____/      ",
    ]
    output = [f"player {x}: {role}"]
    output.extend(racket)
    return "\n".join(output)

@app.route('/')
def index():
    # Show start button on initial page
    return render_template('index2.html')

@app.route('/start_game')
def start_game():
    # Number of players
    players = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # Define roles
    roles = ['mafia', 'mafia', 'mafia',  # 3 mafias
             'citizen', 'citizen', 'citizen', 'citizen', 'citizen',  # 5 citizens
             'killer',  # 1 killer
             'doctor',  # 1 doctor
             'detective']  # 1 detective

    # Shuffle roles to assign them randomly
    random.shuffle(roles)

    # Store players and their roles in the session
    session['players'] = players
    session['roles'] = roles
    session['current_player'] = 0  # Track the current player index
    session['revealed_roles'] = []  # Store revealed roles

    return jsonify({"message": "Game Started! Click 'Reveal First Player' to continue.", "start": True, "players": players, "roles": roles})

@app.route('/reveal_first_player')
def reveal_first_player():
    # Get current player index from session
    current_player_index = session['current_player']
    players = session['players']
    roles = session['roles']
    
    if current_player_index >= len(players):
        return jsonify({"message": "All players have been revealed!", "next_player": None})

    # Get the first player and their role
    player = players[current_player_index]
    role = roles[current_player_index]
    
    # Store the revealed role
    revealed_roles = session.get('revealed_roles', [])
    revealed_roles.append(f"Player {player}: {role}")
    session['revealed_roles'] = revealed_roles

    # Generate the masks
    mask = print_mafia_mask(player)
    open_mask = print_open_mask(player, role)

    return jsonify({
        "mask": mask,
        "open_mask": open_mask,
        "next_player": players[current_player_index + 1] if current_player_index + 1 < len(players) else None
    })

@app.route('/next_player')
def next_player():
    # Get current player index from session
    current_player_index = session['current_player']
    players = session['players']
    roles = session['roles']
    
    if current_player_index >= len(players):
        return jsonify({"message": "All players have been revealed!", "next_player": None})

    # Get the current player and their role
    player = players[current_player_index]
    role = roles[current_player_index]
    
    # Add revealed player role to the session
    revealed_roles = session.get('revealed_roles', [])
    revealed_roles.append(f"Player {player}: {role}")
    session['revealed_roles'] = revealed_roles
    
    # Generate the masks
    mask = print_mafia_mask(player)
    open_mask = print_open_mask(player, role)

    # Move to the next player
    session['current_player'] = current_player_index + 1

    # If all players are revealed, show the list of revealed roles
    if current_player_index + 1 == len(players):
        return jsonify({
            "mask": mask,
            "open_mask": open_mask,
            "revealed_roles": session['revealed_roles'],
            "next_player": None
        })

    return jsonify({
        "mask": mask,
        "open_mask": open_mask,
        "next_player": players[current_player_index + 1] if current_player_index + 1 < len(players) else None
    })

# API route to get players from the database
def get_players():
    import sqlite3
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    rows = cursor.fetchall()
    
    players = []
    for row in rows:
        player = {
            'id': row[0],
            'player_name': row[1],
            'role': row[2],
            'fouls': row[3],
            'healed': row[4]
        }
        players.append(player)
    
    conn.close()
    return players

@app.route('/api/players', methods=['GET'])
def get_players_api():
    # Fetching players from session instead of the database
    players = session.get('players', [])
    roles = session.get('roles', [])
    revealed_roles = session.get('revealed_roles', [])

    # Initialize player data with default values
    player_data = []
    
    for i, player in enumerate(players):
        # Retrieve the role from revealed_roles if it exists
        role = None
        for revealed in revealed_roles:
            if f"Player {player}" in revealed:
                role = revealed.split(": ")[1]  # Extract role from the string like "Player 1: mafia"
                break
        if not role:  # If the role isn't found in revealed_roles, fallback to session roles
            role = roles[i]  # Default to the assigned role if not revealed yet
        
        # Construct player info with revealed role
        player_info = {
            'id': player,  # Assuming player ID is the same as the player number for simplicity
            'player_name': f'Player {player}',  # Placeholder for player name
            'role': role,
            'fouls': 0,  # Placeholder for fouls; you can update this dynamically
            'healed': 0  # Placeholder for healed status
        }
        player_data.append(player_info)
    
    return jsonify(player_data)


@app.route('/update_player/<int:player_id>', methods=['POST'])
def update_player(player_id):
    data = request.get_json()
    fouls = data['fouls']
    healed = data['healed']

    # Update data in the session (or database)
    players = session.get('players', [])
    roles = session.get('roles', [])

    if player_id not in players:
        return jsonify({"success": False, "message": "Player not found."})

    # Find the player index
    player_index = players.index(player_id)
    
    # Update the player info (session-based for this example)
    player_data = session.get('player_data', {})
    if player_id not in player_data:
        player_data[player_id] = {}

    player_data[player_id]['fouls'] = fouls
    player_data[player_id]['healed'] = healed
    session['player_data'] = player_data

    # Optionally, update in the database (if you want it persisted across sessions)
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET fouls = ?, healed = ? WHERE id = ?", (fouls, healed, player_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Player data updated."})



if __name__ == '__main__':
    app.run(debug=True)
    

# chdir "C:\Users\giosa\Downloads\ngrok"  
# ngrok http 5000       