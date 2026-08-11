"""
Database initialization and team seeding.

- init_db(db_path='app.db') -> sqlite3.Connection
"""
import sqlite3

TEAMS = [
    # AL East
    ("Baltimore Orioles", "AL East", "New York Yankees, Boston Red Sox"),
    ("Boston Red Sox", "AL East", "New York Yankees, Tampa Bay Rays"),
    ("New York Yankees", "AL East", "Boston Red Sox, New York Mets"),
    ("Tampa Bay Rays", "AL East", "Boston Red Sox, New York Yankees"),
    ("Toronto Blue Jays", "AL East", "Boston Red Sox, New York Yankees"),
    # AL Central
    ("Chicago White Sox", "AL Central", "Minnesota Twins, Chicago Cubs"),
    ("Cleveland Guardians", "AL Central", "Detroit Tigers, Kansas City Royals"),
    ("Detroit Tigers", "AL Central", "Cleveland Guardians, Kansas City Royals"),
    ("Kansas City Royals", "AL Central", "Detroit Tigers, St. Louis Cardinals"),
    ("Minnesota Twins", "AL Central", "Chicago White Sox, Milwaukee Brewers"),
    # AL West
    ("Houston Astros", "AL West", "Texas Rangers, Los Angeles Angels"),
    ("Los Angeles Angels", "AL West", "Houston Astros, Texas Rangers"),
    ("Oakland Athletics", "AL West", "Seattle Mariners, San Francisco Giants"),
    ("Seattle Mariners", "AL West", "Oakland Athletics, Texas Rangers"),
    ("Texas Rangers", "AL West", "Houston Astros, Los Angeles Angels"),
    # NL East
    ("Atlanta Braves", "NL East", "New York Mets, Philadelphia Phillies"),
    ("Miami Marlins", "NL East", "Atlanta Braves, New York Mets"),
    ("New York Mets", "NL East", "Atlanta Braves, Philadelphia Phillies"),
    ("Philadelphia Phillies", "NL East", "New York Mets"),
    ("Washington Nationals", "NL East", "New York Mets, Philadelphia Phillies"),
    # NL Central
    ("Chicago Cubs", "NL Central", "St. Louis Cardinals, Milwaukee Brewers"),
    ("Cincinnati Reds", "NL Central", "St. Louis Cardinals, Pittsburgh Pirates"),
    ("Milwaukee Brewers", "NL Central", "Chicago Cubs"),
    ("Pittsburgh Pirates", "NL Central", "Cincinnati Reds"),
    ("St. Louis Cardinals", "NL Central", "Chicago Cubs, Cincinnati Reds"),
    # NL West
    ("Arizona Diamondbacks", "NL West", "Los Angeles Dodgers, Colorado Rockies"),
    ("Colorado Rockies", "NL West", "Arizona Diamondbacks"),
    ("Los Angeles Dodgers", "NL West", "San Francisco Giants"),
    ("San Diego Padres", "NL West", "Los Angeles Dodgers"),
    ("San Francisco Giants", "NL West", "Los Angeles Dodgers, Oakland Athletics"),
]

def init_db(db_path: str = "app.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # users: id, username unique, password_hash (BLOB)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash BLOB NOT NULL
    )
    """)
    # teams: id, name unique, division, rivals
    cur.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        division TEXT NOT NULL,
        rivals TEXT
    )
    """)
    conn.commit()
    # seed teams if empty
    cur.execute("SELECT COUNT(*) FROM teams")
    count = cur.fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO teams (name, division, rivals) VALUES (?, ?, ?)",
            TEAMS
        )
        conn.commit()
    return conn

def get_team_by_name(conn: sqlite3.Connection, name: str):
    cur = conn.cursor()
    # exact case-insensitive match
    cur.execute("SELECT name, division, rivals FROM teams WHERE LOWER(name) = LOWER(?)", (name,))
    row = cur.fetchone()
    if row:
        return dict(row)
    # partial match
    cur.execute("SELECT name, division, rivals FROM teams WHERE LOWER(name) LIKE LOWER(?) LIMIT 10", (f"%{name}%",))
    rows = cur.fetchall()
    if rows:
        return [dict(r) for r in rows]
    return None

def list_team_names(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT name FROM teams")
    return [r[0] for r in cur.fetchall()]