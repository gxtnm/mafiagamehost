from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')  # Serve the index.html file from the templates folder

# API route to get players
def get_players():
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
    players = get_players()
    return jsonify(players)

if __name__ == '__main__':
    app.run(debug=True)
