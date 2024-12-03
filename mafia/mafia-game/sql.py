import sqlite3

# Connect to SQLite database (it will create a new database file if it doesn't exist)
conn = sqlite3.connect('players.db')
cursor = conn.cursor()

# Create table with 11 players and columns for 'Role', 'Fouls', and 'Healed'
cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    player_name TEXT NOT NULL,
    role TEXT,
    fouls INTEGER DEFAULT 0,
    healed INTEGER DEFAULT 0
)
''')

# Insert 11 players with empty data for role, fouls, and healed
players = [f"Player {i}" for i in range(1, 12)]
for player in players:
    cursor.execute('''
    INSERT INTO players (player_name, role, fouls, healed)
    VALUES (?, NULL, 0, 0)
    ''', (player,))

# Commit changes and close the connection
conn.commit()

# Fetch and print the contents of the table to verify
cursor.execute("select * FROM players")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()

