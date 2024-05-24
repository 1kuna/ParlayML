
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('sports_betting.db')
c = conn.cursor()

# Create Injuries table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS Injuries (
             player_id INTEGER,
             player_name TEXT,
             team TEXT,
             injury_status TEXT,
             injury_type TEXT,
             expected_return TEXT,
             date TEXT,
             PRIMARY KEY (player_id, date)
             )''')

# Create indexes for quick lookups
c.execute('''CREATE INDEX IF NOT EXISTS idx_team ON Injuries (team)''')
c.execute('''CREATE INDEX IF NOT EXISTS idx_player ON Injuries (player_id)''')

conn.commit()
conn.close()
